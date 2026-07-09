import time
from openai import OpenAI
import random
import jsonlines
from tqdm import tqdm
from transformers import AutoTokenizer
import os

import sys

sys.path.append("../")
from benchmark.dataset.data_loading import load_test, load_articles, get_full_texts, get_titles

if __name__ == "__main__":
    model_name_official = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
    model_name_save = "llama4_scout_17b_16e_instruct"
    target_mode = "test_full"
    # sample_level = "64k" # vllm 75776
    # sample_level = "128k"  # vllm 141312
    # sample_level = "512k"  # vllm 534528
    sample_level = "1024k"  # vllm 1058816

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

    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        )

    tokenizer = AutoTokenizer.from_pretrained(model_name_official)
    for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test), desc=f"{model_name_save}_{sample_level}"):
        if "generations" not in sample.keys():
            question = sample["question"]
            markdowns = get_full_texts(sample, articles_all)
            context = "\n".join(markdowns)
            instruction = open("../benchmark/dataset/instructions/instruction_full_scitrek.txt").read()
            instruction = instruction.replace("<question>", question)

            prompt_content = instruction.replace("<articles>", context)
            while True:
                try:
                    output_dict = client.chat.completions.create(
                        model=model_name_official,
                        messages=[
                            {"role": "user",
                             "content": prompt_content}
                            ],
                        n=3
                        )
                    outputs = []
                    for choice in output_dict.choices:
                        outputs.append(choice.message.content)
                    print([sample["answer"]] + outputs)
                    break
                except Exception as e:
                    print(e)
                    if "limit" in str(e):
                        time.sleep(2)
            sample["generations"] = outputs

            samples_test[sample_index] = sample
            if sample_index % 10 == 0:
                with jsonlines.open(save_name, "w") as writer:
                    writer.write_all(samples_test)

    with jsonlines.open(save_name, "w") as writer:
        writer.write_all(samples_test)

