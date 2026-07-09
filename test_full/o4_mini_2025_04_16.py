import time
from openai import OpenAI
import tiktoken
import jsonlines
from tqdm import tqdm
import os
import sys

sys.path.append("../")
from benchmark.dataset.data_loading import load_test, load_articles, get_full_texts

if __name__ == "__main__":
    model_name_official = "o4-mini-2025-04-16"
    target_mode = "test_full"
    model_name_save = "o4mini_20250416"
    sample_level = "512k"

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

    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    encoding = tiktoken.get_encoding("o200k_base")
    for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test),
                                     desc=f"{model_name_save}_{sample_level}"):
        if "generations" not in sample.keys():
            question = sample["question"]
            markdowns = get_full_texts(sample, articles_all)
            context = "\n".join(markdowns)
            instruction = open("../benchmark/dataset/instructions/instruction_full_scitrek.txt").read()
            instruction = instruction.replace("<question>", question)

            if sample_level in ["512k", "1024k"]:
                max_input_size = 200000
                tokenized_instruction = encoding.encode(instruction, disallowed_special=())
                tokenized_context = encoding.encode(context, disallowed_special=())
                print("tokenized_instruction", len(tokenized_instruction))
                print("tokenized_context", len(tokenized_context))
                if len(tokenized_context) > max_input_size - len(tokenized_instruction):
                    context = encoding.decode(tokenized_context[:max_input_size - len(tokenized_instruction) - 4096])

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