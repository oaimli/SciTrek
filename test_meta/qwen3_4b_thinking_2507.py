import time
from vllm import LLM, SamplingParams
import jsonlines
from tqdm import tqdm
from transformers import AutoTokenizer
import os
import re
import sys

sys.path.append("../")
from bench.dataset.data_loading import load_test, get_tables, load_articles

if __name__ == "__main__":
    COMPILED_REGEX = re.compile(r"\\boxed\{(.*?)\}")
    vllm_tensor_parallel_size = 4

    model_name_official = "Qwen/Qwen3-4B-Thinking-2507"
    model_name_save = "qwen3_4b_thinking_2507"
    target_mode = "test_meta"
    sample_levels = ["64k", "128k", "512k", "1024k"]
    vllm_max_model_length = 65536

    articles_all = load_articles(articles_folder="../bench/article/")

    llm = LLM(model=model_name_official, max_model_len=vllm_max_model_length,
              tensor_parallel_size=vllm_tensor_parallel_size)
    #  max_tokens is for the maximum length for generation.
    sampling_params = SamplingParams(n=3, temperature=0.6, top_p=0.95, top_k=20, max_tokens=10240)
    tokenizer = AutoTokenizer.from_pretrained(model_name_official)

    # testing on different sample levels
    for sample_level in sample_levels:
        save_name = f"../results_test/{sample_level}_{target_mode}_{model_name_save}.jsonl"
        if os.path.exists(save_name):
            samples_test = []
            with jsonlines.open(save_name) as reader:
                for line in reader:
                    samples_test.append(line)
            print("existing results loaded", len(samples_test))
        else:
            samples_test = load_test(prefix=sample_level, samples_folder="../bench/dataset/samples/final/")
            print("original samples loaded", len(samples_test))

        for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test),
                                         desc=f"{model_name_save}_{sample_level}"):
            if "generations" not in sample.keys():
                question = sample["question"]
                table_articles, table_article_author, table_citing_cited = get_tables(sample, articles_all)
                table_articles_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_articles])
                table_article_author_text = "\n".join(
                    [", ".join([str(tmp) for tmp in row]) for row in table_article_author])
                table_citing_cited_text = "\n".join(
                    [", ".join([str(tmp) for tmp in row]) for row in table_citing_cited])

                instruction = open("../benchmark/dataset/instructions/reasoning_instruction.txt").read()
                instruction = instruction.replace("<question>", question)
                instruction = instruction.replace("<table-articles>", table_articles_text)
                instruction = instruction.replace("<table-article_author>", table_article_author_text)
                instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
                prompt_content = instruction
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
