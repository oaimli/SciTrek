import time
from openai import OpenAI
import jsonlines
from tqdm import tqdm
import os

import sys
sys.path.append("../")
from benchmark.dataset.data_loading import load_test, get_tables, load_articles

if __name__ == "__main__":
    model_name_official = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
    model_name_save = "llama4_scout_17b_16e_instruct"
    target_mode = "test_meta"
    sample_levels = ["64k", "128k", "512k", "1024k"]

    articles_all = load_articles(articles_folder="../benchmark/article/")

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
            samples_test = load_test(prefix=sample_level, samples_folder="../benchmark/dataset/samples/final/")
            print("original samples loaded", len(samples_test))

        openai_api_key = "EMPTY"
        openai_api_base = "http://localhost:8000/v1"
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
            )

        for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test), desc=f"{model_name_save}_{sample_level}"):
            if "generations" not in sample.keys():
                question = sample["question"]
                table_articles, table_article_author, table_citing_cited = get_tables(sample, articles_all)
                table_articles_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_articles])
                table_article_author_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_article_author])
                table_citing_cited_text = "\n".join([", ".join([str(tmp) for tmp in row]) for row in table_citing_cited])

                instruction = open("../benchmark/dataset/instructions/instruction_meta_scitrek.txt").read()
                instruction = instruction.replace("<question>", question)
                instruction = instruction.replace("<table-articles>", table_articles_text)
                instruction = instruction.replace("<table-article_author>", table_article_author_text)
                instruction = instruction.replace("<table-citing_cited>", table_citing_cited_text)
                prompt_content = instruction
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

