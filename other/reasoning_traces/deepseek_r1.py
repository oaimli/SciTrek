import jsonlines
import pandas as pd
import random


if __name__ == "__main__":
    # ['articles', 'sample_level', 'sql_type', 'focus', 'sql', 'template', 'question', 'answer', 'label', 'generations', 'reasonings']

    generation_folder = "../../results_test/"

    generations_64k = []
    generations_64k_templates = set([])
    with jsonlines.open(generation_folder + "64k_test_full_deepseek_r1_distill_llama_70b_instruct.jsonl") as reader:
        for line in reader:
            generations_64k.append(line)
            generations_64k_templates.add(line["template"])
    print(len(generations_64k), len(generations_64k_templates)) # 143, 139

    generations_128k = []
    generations_128k_templates = set([])
    with jsonlines.open(generation_folder + "128k_test_full_deepseek_r1_distill_llama_70b_instruct.jsonl") as reader:
        for line in reader:
            generations_128k.append(line)
            generations_128k_templates.add(line["template"])
    print(len(generations_128k), len(generations_128k_templates)) # 883, 779

    templates_intersection = generations_64k_templates.intersection(generations_128k_templates)
    print(len(templates_intersection))

    outputs = []
    for sql_template in templates_intersection:
        print("########SQL template#########")
        outputs.append("########SQL template#########")
        print(sql_template)
        outputs.append(sql_template)
        print("########64k#########")
        for sample in generations_64k:
            if sample["template"] == sql_template:
                outputs.append("########Question on 64k#########")
                outputs.append(sample["question"])
                outputs.append("########Gold answer on 64k#########")
                outputs.append(sample["answer"])
                outputs.append("########Articles on 64k##########")
                outputs.append("_".join(sample["articles"]))
                outputs.append("########Reasoning on 64k#########")
                print(sample["reasonings"][0])
                outputs.append(sample["reasonings"][0])
                break
        print("########128k#########")
        outputs.append("########128k#########")
        for sample in generations_128k:
            if sample["template"] == sql_template:
                outputs.append("########Question on 128k#########")
                outputs.append(sample["question"])
                outputs.append("########Gold answer on 128k#########")
                outputs.append(sample["answer"])
                outputs.append("########Articles on 128k#########")
                outputs.append("_".join(sample["articles"]))
                outputs.append("########Reasoning on 128k#########")
                print(sample["reasonings"][0])
                outputs.append(sample["reasonings"][0])
                break
    output_text = "\n".join(outputs)
    with open("deepseek_r1.txt", "w") as f:
        f.write(output_text)

