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
from bench.dataset.data_loading import load_test, load_articles, get_full_texts

if __name__ == "__main__":
    random.seed(42)
    COMPILED_REGEX = re.compile(r"\\boxed\{(.*?)\}")
    vllm_tensor_parallel_size = 4

    model_name_official = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
    model_name_save = "deepseek_r1_distill_llama_70b_instruct_chunk"
    target_mode = "test_full"
    sample_level = "1024k"
    vllm_max_model_length = 44032
    articles_all = load_articles(articles_folder="../bench/article/")

    llm = LLM(model=model_name_official, max_model_len=vllm_max_model_length,
              tensor_parallel_size=vllm_tensor_parallel_size)
    #  max_tokens is for the maximum length for generation.
    sampling_params = SamplingParams(n=3, temperature=0.6, top_p=0.95, max_tokens=10240)
    tokenizer = AutoTokenizer.from_pretrained(model_name_official)
    print(tokenizer.chat_template)

    save_name = f"../results_test/{sample_level}_{target_mode}_{model_name_save}_150.jsonl"
    if os.path.exists(save_name):
        samples_test = []
        with jsonlines.open(save_name) as reader:
            for line in reader:
                samples_test.append(line)
        print("existing results loaded", len(samples_test))
    else:
        samples_test = load_test(prefix=sample_level, samples_folder="../bench/dataset/samples/final/")
        samples_test = random.sample(samples_test, 300)
        print("original samples loaded", len(samples_test))

    for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test),
                                     desc=f"{model_name_save}_{sample_level}"):
        if "generations" not in sample.keys() and sample_index >= 150:
            question = sample["question"]
            markdowns = get_full_texts(sample, articles_all)
            context = "\n".join(markdowns)
            instruction = open("../benchmark/dataset/instructions/reasoning_instruction.txt").read()
            instruction = instruction.replace("<question>", question)

            generations = []
            reasonings = []
            tokenized_context = tokenizer.encode(context)
            print("tokenized_context", len(tokenized_context))
            chunk = []
            for token_index, token in enumerate(tokenized_context):
                chunk.append(token)
                if len(chunk) ==32*1024 or token_index == len(tokenized_context)-1:
                    print("chunk", len(chunk))
                    context = tokenizer.decode(chunk)
                    prompt_content = instruction.replace("<articles>", context)
                    conversation = [{"role": "user", "content": prompt_content}]
                    text = tokenizer.apply_chat_template(
                        conversation,
                        tokenize=False,
                        add_generation_prompt=True
                        )
                    conversation_outputs = llm.generate([text], sampling_params, use_tqdm=False)
                    # print(conversation_outputs)
                    for conversation_output in conversation_outputs:
                        for tmp in conversation_output.outputs:
                            matches = COMPILED_REGEX.findall(tmp.text)
                            answer = matches[-1] if matches else ""
                            generations.append(answer)
                            reasonings.append(tmp.text)
                    chunk = []

            sample["generations"] = generations
            sample["reasonings"] = reasonings
            print([sample["answer"]] + sample["generations"])

            samples_test[sample_index] = sample
            if sample_index % 10 == 0:
                with jsonlines.open(save_name, "w") as writer:
                    writer.write_all(samples_test)

        with jsonlines.open(save_name, "w") as writer:
            writer.write_all(samples_test)

