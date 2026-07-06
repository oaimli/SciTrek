import pandas as pd
import json
import random
import jsonlines
import json
import os
import sys

sys.path.append("../../")
from bench.dataset.data_loading import load_articles, get_tables

if __name__ == "__main__":
    random.seed(42)
    sft_result_folder = "../../train_sft/input_length/generations"
    samples_qwen25_7b_instruct_1m_sft = []
    with jsonlines.open(os.path.join(sft_result_folder, "128k_test_full_qwen25_7b_instruct_1m_sft.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen25_7b_instruct_1m_sft.append(line)
    print("samples_qwen25_7b_instruct_1m_sft", len(samples_qwen25_7b_instruct_1m_sft))

    grpo_result_folder = "../../train_grpo/grpo/generations_sampled_192"
    samples_qwen25_7b_instruct_1m_grpo = []
    with jsonlines.open(os.path.join(grpo_result_folder, "128k_test_full_qwen25_7b_instruct_1m_grpo.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen25_7b_instruct_1m_grpo.append(line)
    print("samples_qwen25_7b_instruct_1m_grpo", len(samples_qwen25_7b_instruct_1m_grpo))

    test_result_folder = "../../results_test/"
    samples_gemini25_pro = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_gemini25_pro.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_gemini25_pro.append(line)
    print("samples_gemini25_pro", len(samples_gemini25_pro))
    samples_gemma3_27b_it = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_gemma3_27b_it.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_gemma3_27b_it.append(line)
    print("samples_gemma3_27b_it", len(samples_gemma3_27b_it))
    samples_gpt41_20250414 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_gpt41_20250414.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_gpt41_20250414.append(line)
    print("samples_gpt41_20250414", len(samples_gpt41_20250414))
    samples_llama33_70b_instruct = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_llama33_70b_instruct.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_llama33_70b_instruct.append(line)
    print("samples_llama33_70b_instruct", len(samples_llama33_70b_instruct))
    samples_llama4_scout_17b_16e_instruct = []
    with jsonlines.open(
            os.path.join(test_result_folder, "128k_test_full_llama4_scout_17b_16e_instruct.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_llama4_scout_17b_16e_instruct.append(line)
    print("samples_llama4_scout_17b_16e_instruct", len(samples_llama4_scout_17b_16e_instruct))
    samples_o4mini_20250416 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_o4mini_20250416.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_o4mini_20250416.append(line)
    print("samples_o4mini_20250416", len(samples_o4mini_20250416))
    samples_qwen25_14b_instruct_1m = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen25_14b_instruct_1m.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen25_14b_instruct_1m.append(line)
    print("samples_qwen25_14b_instruct_1m", len(samples_qwen25_14b_instruct_1m))
    samples_qwen25_7b_instruct_1m = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen25_7b_instruct_1m.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen25_7b_instruct_1m.append(line)
    print("samples_qwen25_7b_instruct_1m", len(samples_qwen25_7b_instruct_1m))
    samples_deepseek_r1_distill_llama_70b_instruct = []
    with jsonlines.open(
            os.path.join(test_result_folder, "128k_test_full_deepseek_r1_distill_llama_70b_instruct.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_deepseek_r1_distill_llama_70b_instruct.append(line)
    print("samples_deepseek_r1_distill_llama_70b_instruct", len(samples_deepseek_r1_distill_llama_70b_instruct))

    samples_qwen3_4b_instruct_2507 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen3_4b_instruct_2507.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen3_4b_instruct_2507.append(line)
    print("samples_qwen3_4b_instruct_2507", len(samples_qwen3_4b_instruct_2507))
    samples_qwen3_4b_thinking_2507 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen3_4b_thinking_2507.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen3_4b_thinking_2507.append(line)
    print("samples_qwen3_4b_thinking_2507", len(samples_qwen3_4b_thinking_2507))
    samples_qwen3_30b_a3b_instruct_2507 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen3_30b_a3b_instruct_2507.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen3_30b_a3b_instruct_2507.append(line)
    print("samples_qwen3_30b_a3b_instruct_2507", len(samples_qwen3_30b_a3b_instruct_2507))
    samples_qwen3_30b_a3b_thinking_2507 = []
    with jsonlines.open(os.path.join(test_result_folder, "128k_test_full_qwen3_30b_a3b_thinking_2507.jsonl")) as reader:
        for line in reader:
            if line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                samples_qwen3_30b_a3b_thinking_2507.append(line)
    print("samples_qwen3_30b_a3b_thinking_2507", len(samples_qwen3_30b_a3b_thinking_2507))

    articles = load_articles(articles_folder="../../bench/article/")


    def preprocessing_answer(generation):
        generation = str(generation)
        generation = generation.strip()
        generation = " ".join(generation.split())
        generation = ", ".join([tmp.strip() for tmp in generation.split(",")])
        return generation


    samples_aggregating = []
    samples_sorting = []
    samples_filtering = []
    samples_filtering_sorting = []
    samples_filtering_aggregating = []
    samples_rational_filtering = []
    for qwen25_7b_instruct_1m_sft, qwen25_7b_instruct_1m_grpo, gemini25_pro, gemma3_27b_it, gpt41_20250414, llama33_70b_instruct, llama4_scout_17b_16e_instruct, o4mini_20250416, qwen25_14b_instruct_1m, qwen25_7b_instruct_1m, deepseek_r1_distill_llama_70b_instruct, qwen3_4b_instruct_2507, qwen3_4b_thinking_2507, qwen3_30b_a3b_instruct_2507, qwen3_30b_a3b_thinking_2507 in zip(
            samples_qwen25_7b_instruct_1m_sft, samples_qwen25_7b_instruct_1m_grpo,
            samples_gemini25_pro, samples_gemma3_27b_it, samples_gpt41_20250414, samples_llama33_70b_instruct,
            samples_llama4_scout_17b_16e_instruct, samples_o4mini_20250416, samples_qwen25_14b_instruct_1m,
            samples_qwen25_7b_instruct_1m, samples_deepseek_r1_distill_llama_70b_instruct,
            samples_qwen3_4b_instruct_2507, samples_qwen3_4b_thinking_2507, samples_qwen3_30b_a3b_instruct_2507,
            samples_qwen3_30b_a3b_thinking_2507):
        question = qwen25_7b_instruct_1m_sft["question"]
        ground_truth_answer = qwen25_7b_instruct_1m_sft["answer"]
        sql_type = qwen25_7b_instruct_1m_sft["sql_type"]
        table_articles, table_article_author, table_citing_cited = get_tables(qwen25_7b_instruct_1m_sft, articles)

        tmp = {}
        tmp["question"] = question
        tmp["sql_type"] = sql_type
        tmp["articles"] = table_articles
        tmp["article_author"] = table_article_author
        tmp["citing_cited"] = table_citing_cited
        tmp["ground_truth_answer"] = ground_truth_answer
        tmp["qwen25_7b_instruct_1m_sft"] = preprocessing_answer(random.choice(qwen25_7b_instruct_1m_sft["generations"]))
        tmp["qwen25_7b_instruct_1m_grpo"] = preprocessing_answer(
            random.choice(qwen25_7b_instruct_1m_grpo["generations"]))
        tmp["gemini25_pro"] = preprocessing_answer(random.choice(gemini25_pro["generations"]))
        tmp["gemma3_27b_it"] = preprocessing_answer(random.choice(gemma3_27b_it["generations"]))
        tmp["gpt41_20250414"] = preprocessing_answer(random.choice(gpt41_20250414["generations"]))
        tmp["llama33_70b_instruct"] = preprocessing_answer(random.choice(llama33_70b_instruct["generations"]))
        tmp["llama4_scout_17b_16e_instruct"] = preprocessing_answer(
            random.choice(llama4_scout_17b_16e_instruct["generations"]))
        tmp["o4mini_20250416"] = preprocessing_answer(random.choice(o4mini_20250416["generations"]))
        tmp["qwen25_14b_instruct_1m"] = preprocessing_answer(random.choice(qwen25_14b_instruct_1m["generations"]))
        tmp["qwen25_7b_instruct_1m"] = preprocessing_answer(random.choice(qwen25_7b_instruct_1m["generations"]))
        tmp["deepseek_r1_distill_llama_70b_instruct"] = preprocessing_answer(
            random.choice(deepseek_r1_distill_llama_70b_instruct["generations"]))
        tmp["qwen3_4b_instruct_2507"] = preprocessing_answer(
            random.choice(qwen3_4b_instruct_2507["generations"]))
        tmp["qwen3_4b_thinking_2507"] = preprocessing_answer(
            random.choice(qwen3_4b_thinking_2507["generations"]))
        tmp["qwen3_30b_a3b_instruct_2507"] = preprocessing_answer(
            random.choice(qwen3_30b_a3b_instruct_2507["generations"]))
        tmp["qwen3_30b_a3b_thinking_2507"] = preprocessing_answer(
            random.choice(qwen3_30b_a3b_thinking_2507["generations"]))

        if ground_truth_answer not in [tmp["qwen25_7b_instruct_1m_sft"], tmp["qwen25_7b_instruct_1m_grpo"],
                                       tmp["gemini25_pro"], tmp["gemma3_27b_it"], tmp["gpt41_20250414"],
                                       tmp["llama33_70b_instruct"], tmp["llama4_scout_17b_16e_instruct"],
                                       tmp["o4mini_20250416"], tmp["qwen25_14b_instruct_1m"],
                                       tmp["qwen25_7b_instruct_1m"], tmp["deepseek_r1_distill_llama_70b_instruct"],
                                       tmp["qwen3_4b_instruct_2507"], tmp["qwen3_4b_thinking_2507"],
                                       tmp["qwen3_30b_a3b_instruct_2507"], tmp["qwen3_30b_a3b_thinking_2507"]]:
            if sql_type == "multi_ran_filtering_ofo":
                samples_filtering.append(tmp)
            elif sql_type == "multi_ran_filtering_foo":
                samples_filtering_sorting.append(tmp)
            elif sql_type == "multi_ran_filtering_foa":
                samples_filtering_aggregating.append(tmp)
            elif sql_type == "multi_ran_aggregating":
                samples_aggregating.append(tmp)
            elif sql_type == "multi_ran_organizing":
                samples_sorting.append(tmp)
            elif sql_type == "multi_graph_filtering":
                samples_rational_filtering.append(tmp)
            else:
                print("unknown sql type", sql_type)
    print(len(samples_aggregating), len(samples_sorting), len(samples_filtering), len(samples_filtering_aggregating),
          len(samples_filtering_sorting), len(samples_rational_filtering))

    samples_final = []
    samples_final.extend(random.sample(samples_aggregating, 10))
    samples_final.extend(random.sample(samples_sorting, 10))
    samples_final.extend(random.sample(samples_filtering, 10))
    samples_final.extend(random.sample(samples_filtering_aggregating, 10))
    samples_final.extend(random.sample(samples_filtering_sorting, 10))
    samples_final.extend(random.sample(samples_rational_filtering, 10))

    failures = []
    failures.append(
        ["Sample", "qwen25_7b_instruct_1m_sft", "qwen25_7b_instruct_1m_grpo", "gemini25_pro", "gemma3_27b_it",
         "gpt41_20250414", "llama33_70b_instruct", "llama4_scout_17b_16e_instruct", "o4mini_20250416",
         "qwen25_14b_instruct_1m", "qwen25_7b_instruct_1m", "deepseek_r1_distill_llama_70b_instruct",
         "qwen3_4b_instruct_2507", "qwen3_4b_thinking_2507", "qwen3_30b_a3b_instruct_2507",
         "qwen3_30b_a3b_thinking_2507"])
    for i, sample in enumerate(samples_final):
        tmp = []
        tmp.append(f"sample_{i}")

        if sample["qwen25_7b_instruct_1m_sft"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen25_7b_instruct_1m_sft"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen25_7b_instruct_1m_sft"] in sample["ground_truth_answer"] and sample[
            "qwen25_7b_instruct_1m_sft"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen25_7b_instruct_1m_sft"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen25_7b_instruct_1m_grpo"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen25_7b_instruct_1m_grpo"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen25_7b_instruct_1m_grpo"] in sample["ground_truth_answer"] and sample[
            "qwen25_7b_instruct_1m_grpo"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen25_7b_instruct_1m_grpo"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["gemini25_pro"] == "NULL":
            tmp.append("NULLL")
        elif sample["gemini25_pro"].strip() == "":
            tmp.append("EMPTY")
        elif sample["gemini25_pro"] in sample["ground_truth_answer"] and sample[
            "gemini25_pro"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["gemini25_pro"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["gemma3_27b_it"] == "NULL":
            tmp.append("NULLL")
        elif sample["gemma3_27b_it"].strip() == "":
            tmp.append("EMPTY")
        elif sample["gemma3_27b_it"] in sample["ground_truth_answer"] and sample[
            "gemma3_27b_it"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["gemma3_27b_it"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["gpt41_20250414"] == "NULL":
            tmp.append("NULLL")
        elif sample["gpt41_20250414"].strip() == "":
            tmp.append("EMPTY")
        elif sample["gpt41_20250414"] in sample["ground_truth_answer"] and sample[
            "gpt41_20250414"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["gpt41_20250414"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["llama33_70b_instruct"] == "NULL":
            tmp.append("NULLL")
        elif sample["llama33_70b_instruct"].strip() == "":
            tmp.append("EMPTY")
        elif sample["llama33_70b_instruct"] in sample["ground_truth_answer"] and sample[
            "llama33_70b_instruct"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["llama33_70b_instruct"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["llama4_scout_17b_16e_instruct"] == "NULL":
            tmp.append("NULLL")
        elif sample["llama4_scout_17b_16e_instruct"].strip() == "":
            tmp.append("EMPTY")
        elif sample["llama4_scout_17b_16e_instruct"] in sample["ground_truth_answer"] and sample[
            "llama4_scout_17b_16e_instruct"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["llama4_scout_17b_16e_instruct"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["o4mini_20250416"] == "NULL":
            tmp.append("NULLL")
        elif sample["o4mini_20250416"].strip() == "":
            tmp.append("EMPTY")
        elif sample["o4mini_20250416"] in sample["ground_truth_answer"] and sample[
            "o4mini_20250416"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["o4mini_20250416"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen25_14b_instruct_1m"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen25_14b_instruct_1m"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen25_14b_instruct_1m"] in sample["ground_truth_answer"] and sample[
            "qwen25_14b_instruct_1m"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen25_14b_instruct_1m"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen25_7b_instruct_1m"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen25_7b_instruct_1m"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen25_7b_instruct_1m"] in sample["ground_truth_answer"] and sample[
            "qwen25_7b_instruct_1m"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen25_7b_instruct_1m"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["deepseek_r1_distill_llama_70b_instruct"] == "NULL":
            tmp.append("NULLL")
        elif sample["deepseek_r1_distill_llama_70b_instruct"].strip() == "":
            tmp.append("EMPTY")
        elif sample["deepseek_r1_distill_llama_70b_instruct"] in sample["ground_truth_answer"] and sample[
            "deepseek_r1_distill_llama_70b_instruct"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["deepseek_r1_distill_llama_70b_instruct"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen3_4b_instruct_2507"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen3_4b_instruct_2507"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen3_4b_instruct_2507"] in sample["ground_truth_answer"] and sample[
            "qwen3_4b_instruct_2507"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen3_4b_instruct_2507"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen3_4b_thinking_2507"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen3_4b_thinking_2507"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen3_4b_thinking_2507"] in sample["ground_truth_answer"] and sample[
            "qwen3_4b_thinking_2507"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen3_4b_thinking_2507"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen3_30b_a3b_instruct_2507"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen3_30b_a3b_instruct_2507"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen3_30b_a3b_instruct_2507"] in sample["ground_truth_answer"] and sample[
            "qwen3_30b_a3b_instruct_2507"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen3_30b_a3b_instruct_2507"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        if sample["qwen3_30b_a3b_thinking_2507"] == "NULL":
            tmp.append("NULLL")
        elif sample["qwen3_30b_a3b_thinking_2507"].strip() == "":
            tmp.append("EMPTY")
        elif sample["qwen3_30b_a3b_thinking_2507"] in sample["ground_truth_answer"] and sample[
            "qwen3_30b_a3b_thinking_2507"] != "":
            tmp.append("LESS")
        elif sample["ground_truth_answer"] in sample["qwen3_30b_a3b_thinking_2507"]:
            tmp.append("MORE")
        else:
            tmp.append("")

        failures.append(tmp)

    df = pd.DataFrame(failures)
    df.to_excel("analysis.xlsx", sheet_name="failures", index=False)

    if not os.path.isdir("tables"):
        os.mkdir("tables")
    for i, sample in enumerate(samples_final):
        sample["index"] = i
        table_articles = sample["articles"]
        table_article_author = sample["article_author"]
        table_citing_cited = sample["citing_cited"]
        del sample["articles"]
        del sample["article_author"]
        del sample["citing_cited"]
        samples_final[i] = sample

        with pd.ExcelWriter(f"tables/sample_{i}.xlsx") as writer:
            df = pd.DataFrame(table_articles[1:], columns=table_articles[0])
            df.to_excel(writer, sheet_name="articles", index=False)

            df = pd.DataFrame(table_article_author[1:], columns=table_article_author[0])
            df.to_excel(writer, sheet_name="article_author", index=False)

            df = pd.DataFrame(table_citing_cited[1:], columns=table_citing_cited[0])
            df.to_excel(writer, sheet_name="citing_cited", index=False)

    with open("case_study.json", "w") as f:
        json.dump(samples_final, f, indent=4)
