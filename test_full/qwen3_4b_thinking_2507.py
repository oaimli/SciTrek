import time
from vllm import LLM, SamplingParams
import random
import jsonlines
from tqdm import tqdm
from transformers import AutoTokenizer
import os
import re
import sys

sys.path.append("../")
from benchmark.dataset.data_loading import load_test, load_articles, get_full_texts, get_titles

if __name__ == "__main__":
    COMPILED_REGEX = re.compile(r"\\boxed\{(.*?)\}")
    vllm_tensor_parallel_size = 4

    model_name_official = "Qwen/Qwen3-4B-Thinking-2507"
    model_name_save = "qwen3_4b_thinking_2507"
    target_mode = "test_full"
    sample_level = "64k"
    vllm_max_model_length = 75776

    # sample_level = "128k"
    # vllm_max_model_length = 131072

    articles_all = load_articles(articles_folder="../benchmark/article/")

    save_name = f"../results_test/{sample_level}_{target_mode}_{model_name_save}.jsonl"
    if os.path.exists(save_name):
        samples_test = []
        with jsonlines.open(save_name) as reader:
            for line in reader:
                samples_test.append(line)
        print("existing results loaded", len(samples_test))
    else:
        samples_test = load_test(prefix=sample_level, samples_folder="../benchmark/dataset/samples/final/")
        print("original samples loaded", len(samples_test))

    llm = LLM(model=model_name_official, max_model_len=vllm_max_model_length,
              tensor_parallel_size=vllm_tensor_parallel_size)
    #  max_tokens is for the maximum length for generation.
    sampling_params = SamplingParams(n=3, temperature=0.6, top_p=0.95, top_k=20, max_tokens=10240)

    tokenizer = AutoTokenizer.from_pretrained(model_name_official)
    print(tokenizer.chat_template)
    for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test),
                                     desc=f"{model_name_save}_{sample_level}"):
        if "generations" not in sample.keys():
            question = sample["question"]
            markdowns = get_full_texts(sample, articles_all)
            context = "\n".join(markdowns)
            instruction = open("../benchmark/dataset/instructions/reasoning_instruction_full_scitrek.txt").read()
            instruction = instruction.replace("<question>", question)

            # truncate the input texts when model context is larger than the sample level
            if sample_level == "128k":
                model_max_window = 131072
                tokenized_instruction = tokenizer.encode(instruction)
                print("tokenized_instruction", len(tokenized_instruction))

                # the max generation size is set to the number of title tokens in all input articles
                titles = get_titles(sample, articles_all)
                tokenized_titles = tokenizer.encode(", ".join(titles))
                input_size = model_max_window - len(tokenized_titles) * 2 - len(tokenized_instruction)

                tokenized_context = tokenizer.encode(context)
                print("tokenized_context", len(tokenized_context))
                if len(tokenized_context) > input_size: # no data is truncated
                    context = tokenizer.decode(tokenized_context[:input_size])
                    print("context truncated", len(tokenized_context), input_size)
            prompt_content = instruction.replace("<articles>", context)

            conversation = [{"role": "user", "content": prompt_content}]
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
                )
            conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
            # print(conversation_outputs)
            generations = []
            reasonings = []
            for conversation_output in conversation_outputs:
                for tmp in conversation_output.outputs:
                    matches = COMPILED_REGEX.findall(tmp.text)
                    answer = matches[-1] if matches else ""
                    generations.append(answer)
                    reasonings.append(tmp.text)

            sample["generations"] = generations
            sample["reasonings"] = reasonings
            print([sample["answer"]] + sample["generations"])
            samples_test[sample_index] = sample
            if sample_index % 10 == 0:
                with jsonlines.open(save_name, "w") as writer:
                    writer.write_all(samples_test)

    with jsonlines.open(save_name, "w") as writer:
        writer.write_all(samples_test)

