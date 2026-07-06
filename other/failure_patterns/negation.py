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

        if "not" in question or "never" in question:
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

    print("filtering", len(samples_filtering))
    total_number = len(samples_filtering)
    qwen25_7b_instruct_1m_sft = []
    qwen25_7b_instruct_1m_grpo = []
    gemini25_pro = []
    gemma3_27b_it = []
    gpt41_20250414 = []
    llama33_70b_instruct = []
    llama4_scout_17b_16e_instruct = []
    o4mini_20250416 = []
    qwen25_14b_instruct_1m = []
    qwen25_7b_instruct_1m = []
    deepseek_r1_distill_llama_70b_instruct = []
    qwen3_4b_instruct_2507 = []
    qwen3_4b_thinking_2507 = []
    qwen3_30b_a3b_instruct_2507 = []
    qwen3_30b_a3b_thinking_2507 = []
    for sample in samples_aggregating:
        ground_truth_answer = sample["ground_truth_answer"]
        if sample["qwen25_7b_instruct_1m_sft"] == ground_truth_answer:
            qwen25_7b_instruct_1m_sft.append(1)
        if sample["qwen25_7b_instruct_1m_grpo"] == ground_truth_answer:
            qwen25_7b_instruct_1m_grpo.append(1)
        if sample["gemini25_pro"] == ground_truth_answer:
            gemini25_pro.append(1)
        if sample["gemma3_27b_it"] == ground_truth_answer:
            gemma3_27b_it.append(1)
        if sample["gpt41_20250414"] == ground_truth_answer:
            gpt41_20250414.append(1)
        if sample["llama33_70b_instruct"] == ground_truth_answer:
            llama33_70b_instruct.append(1)
        if sample["llama4_scout_17b_16e_instruct"] == ground_truth_answer:
            llama4_scout_17b_16e_instruct.append(1)
        if sample["o4mini_20250416"] == ground_truth_answer:
            o4mini_20250416.append(1)
        if sample["qwen25_14b_instruct_1m"] == ground_truth_answer:
            qwen25_14b_instruct_1m.append(1)
        if sample["qwen25_7b_instruct_1m"] == ground_truth_answer:
            qwen25_7b_instruct_1m.append(1)
        if sample["deepseek_r1_distill_llama_70b_instruct"] == ground_truth_answer:
            deepseek_r1_distill_llama_70b_instruct.append(1)
        if sample["qwen3_4b_instruct_2507"] == ground_truth_answer:
            qwen3_4b_instruct_2507.append(1)
        if sample["qwen3_4b_thinking_2507"] == ground_truth_answer:
            qwen3_4b_thinking_2507.append(1)
        if sample["qwen3_30b_a3b_instruct_2507"] == ground_truth_answer:
            qwen3_30b_a3b_instruct_2507.append(1)
        if sample["qwen3_30b_a3b_thinking_2507"] == ground_truth_answer:
            qwen3_30b_a3b_thinking_2507.append(1)
    print("qwen25_7b_instruct_1m_sft", len(qwen25_7b_instruct_1m_sft) / total_number)
    print("qwen25_7b_instruct_1m_grpo", len(qwen25_7b_instruct_1m_grpo) / total_number)
    print("gemini25_pro", len(gemini25_pro) / total_number)
    print("gemma3_27b_it", len(gemma3_27b_it) / total_number)
    print("gpt41_20250414", len(gpt41_20250414) / total_number)
    print("llama33_70b_instruct", len(llama33_70b_instruct) / total_number)
    print("llama4_scout_17b_16e_instruct", len(llama4_scout_17b_16e_instruct) / total_number)
    print("o4mini_20250416", len(o4mini_20250416) / total_number)
    print("qwen25_14b_instruct_1m", len(qwen25_14b_instruct_1m) / total_number)
    print("qwen25_7b_instruct_1m", len(qwen25_7b_instruct_1m) / total_number)
    print("deepseek_r1_distill_llama_70b_instruct", len(deepseek_r1_distill_llama_70b_instruct) / total_number)
    print("qwen3_4b_instruct_2507", len(qwen3_4b_instruct_2507) / total_number)
    print("qwen3_4b_thinking_2507", len(qwen3_4b_thinking_2507) / total_number)
    print("qwen3_30b_a3b_instruct_2507", len(qwen3_30b_a3b_instruct_2507) / total_number)
    print("qwen3_30b_a3b_thinking_2507", len(qwen3_30b_a3b_thinking_2507) / total_number)

    print("filtering+aggregating", len(samples_filtering_aggregating))
    total_number = len(samples_filtering_aggregating)
    qwen25_7b_instruct_1m_sft = []
    qwen25_7b_instruct_1m_grpo = []
    gemini25_pro = []
    gemma3_27b_it = []
    gpt41_20250414 = []
    llama33_70b_instruct = []
    llama4_scout_17b_16e_instruct = []
    o4mini_20250416 = []
    qwen25_14b_instruct_1m = []
    qwen25_7b_instruct_1m = []
    deepseek_r1_distill_llama_70b_instruct = []
    qwen3_4b_instruct_2507 = []
    qwen3_4b_thinking_2507 = []
    qwen3_30b_a3b_instruct_2507 = []
    qwen3_30b_a3b_thinking_2507 = []
    for sample in samples_filtering_aggregating:
        ground_truth_answer = sample["ground_truth_answer"]
        if sample["qwen25_7b_instruct_1m_sft"] == ground_truth_answer:
            qwen25_7b_instruct_1m_sft.append(1)
        if sample["qwen25_7b_instruct_1m_grpo"] == ground_truth_answer:
            qwen25_7b_instruct_1m_grpo.append(1)
        if sample["gemini25_pro"] == ground_truth_answer:
            gemini25_pro.append(1)
        if sample["gemma3_27b_it"] == ground_truth_answer:
            gemma3_27b_it.append(1)
        if sample["gpt41_20250414"] == ground_truth_answer:
            gpt41_20250414.append(1)
        if sample["llama33_70b_instruct"] == ground_truth_answer:
            llama33_70b_instruct.append(1)
        if sample["llama4_scout_17b_16e_instruct"] == ground_truth_answer:
            llama4_scout_17b_16e_instruct.append(1)
        if sample["o4mini_20250416"] == ground_truth_answer:
            o4mini_20250416.append(1)
        if sample["qwen25_14b_instruct_1m"] == ground_truth_answer:
            qwen25_14b_instruct_1m.append(1)
        if sample["qwen25_7b_instruct_1m"] == ground_truth_answer:
            qwen25_7b_instruct_1m.append(1)
        if sample["deepseek_r1_distill_llama_70b_instruct"] == ground_truth_answer:
            deepseek_r1_distill_llama_70b_instruct.append(1)
        if sample["qwen3_4b_instruct_2507"] == ground_truth_answer:
            qwen3_4b_instruct_2507.append(1)
        if sample["qwen3_4b_thinking_2507"] == ground_truth_answer:
            qwen3_4b_thinking_2507.append(1)
        if sample["qwen3_30b_a3b_instruct_2507"] == ground_truth_answer:
            qwen3_30b_a3b_instruct_2507.append(1)
        if sample["qwen3_30b_a3b_thinking_2507"] == ground_truth_answer:
            qwen3_30b_a3b_thinking_2507.append(1)
    print("qwen25_7b_instruct_1m_sft", len(qwen25_7b_instruct_1m_sft) / total_number)
    print("qwen25_7b_instruct_1m_grpo", len(qwen25_7b_instruct_1m_grpo) / total_number)
    print("gemini25_pro", len(gemini25_pro) / total_number)
    print("gemma3_27b_it", len(gemma3_27b_it) / total_number)
    print("gpt41_20250414", len(gpt41_20250414) / total_number)
    print("llama33_70b_instruct", len(llama33_70b_instruct) / total_number)
    print("llama4_scout_17b_16e_instruct", len(llama4_scout_17b_16e_instruct) / total_number)
    print("o4mini_20250416", len(o4mini_20250416) / total_number)
    print("qwen25_14b_instruct_1m", len(qwen25_14b_instruct_1m) / total_number)
    print("qwen25_7b_instruct_1m", len(qwen25_7b_instruct_1m) / total_number)
    print("deepseek_r1_distill_llama_70b_instruct", len(deepseek_r1_distill_llama_70b_instruct) / total_number)
    print("qwen3_4b_instruct_2507", len(qwen3_4b_instruct_2507) / total_number)
    print("qwen3_4b_thinking_2507", len(qwen3_4b_thinking_2507) / total_number)
    print("qwen3_30b_a3b_instruct_2507", len(qwen3_30b_a3b_instruct_2507) / total_number)
    print("qwen3_30b_a3b_thinking_2507", len(qwen3_30b_a3b_thinking_2507) / total_number)

    print("filtering+sorting", len(samples_filtering_sorting))
    total_number = len(samples_filtering_sorting)
    qwen25_7b_instruct_1m_sft = []
    qwen25_7b_instruct_1m_grpo = []
    gemini25_pro = []
    gemma3_27b_it = []
    gpt41_20250414 = []
    llama33_70b_instruct = []
    llama4_scout_17b_16e_instruct = []
    o4mini_20250416 = []
    qwen25_14b_instruct_1m = []
    qwen25_7b_instruct_1m = []
    deepseek_r1_distill_llama_70b_instruct = []
    qwen3_4b_instruct_2507 = []
    qwen3_4b_thinking_2507 = []
    qwen3_30b_a3b_instruct_2507 = []
    qwen3_30b_a3b_thinking_2507 = []
    for sample in samples_filtering_sorting:
        ground_truth_answer = sample["ground_truth_answer"]
        if sample["qwen25_7b_instruct_1m_sft"] == ground_truth_answer:
            qwen25_7b_instruct_1m_sft.append(1)
        if sample["qwen25_7b_instruct_1m_grpo"] == ground_truth_answer:
            qwen25_7b_instruct_1m_grpo.append(1)
        if sample["gemini25_pro"] == ground_truth_answer:
            gemini25_pro.append(1)
        if sample["gemma3_27b_it"] == ground_truth_answer:
            gemma3_27b_it.append(1)
        if sample["gpt41_20250414"] == ground_truth_answer:
            gpt41_20250414.append(1)
        if sample["llama33_70b_instruct"] == ground_truth_answer:
            llama33_70b_instruct.append(1)
        if sample["llama4_scout_17b_16e_instruct"] == ground_truth_answer:
            llama4_scout_17b_16e_instruct.append(1)
        if sample["o4mini_20250416"] == ground_truth_answer:
            o4mini_20250416.append(1)
        if sample["qwen25_14b_instruct_1m"] == ground_truth_answer:
            qwen25_14b_instruct_1m.append(1)
        if sample["qwen25_7b_instruct_1m"] == ground_truth_answer:
            qwen25_7b_instruct_1m.append(1)
        if sample["deepseek_r1_distill_llama_70b_instruct"] == ground_truth_answer:
            deepseek_r1_distill_llama_70b_instruct.append(1)
        if sample["qwen3_4b_instruct_2507"] == ground_truth_answer:
            qwen3_4b_instruct_2507.append(1)
        if sample["qwen3_4b_thinking_2507"] == ground_truth_answer:
            qwen3_4b_thinking_2507.append(1)
        if sample["qwen3_30b_a3b_instruct_2507"] == ground_truth_answer:
            qwen3_30b_a3b_instruct_2507.append(1)
        if sample["qwen3_30b_a3b_thinking_2507"] == ground_truth_answer:
            qwen3_30b_a3b_thinking_2507.append(1)
    print("qwen25_7b_instruct_1m_sft", len(qwen25_7b_instruct_1m_sft) / total_number)
    print("qwen25_7b_instruct_1m_grpo", len(qwen25_7b_instruct_1m_grpo) / total_number)
    print("gemini25_pro", len(gemini25_pro) / total_number)
    print("gemma3_27b_it", len(gemma3_27b_it) / total_number)
    print("gpt41_20250414", len(gpt41_20250414) / total_number)
    print("llama33_70b_instruct", len(llama33_70b_instruct) / total_number)
    print("llama4_scout_17b_16e_instruct", len(llama4_scout_17b_16e_instruct) / total_number)
    print("o4mini_20250416", len(o4mini_20250416) / total_number)
    print("qwen25_14b_instruct_1m", len(qwen25_14b_instruct_1m) / total_number)
    print("qwen25_7b_instruct_1m", len(qwen25_7b_instruct_1m) / total_number)
    print("deepseek_r1_distill_llama_70b_instruct", len(deepseek_r1_distill_llama_70b_instruct) / total_number)
    print("qwen3_4b_instruct_2507", len(qwen3_4b_instruct_2507) / total_number)
    print("qwen3_4b_thinking_2507", len(qwen3_4b_thinking_2507) / total_number)
    print("qwen3_30b_a3b_instruct_2507", len(qwen3_30b_a3b_instruct_2507) / total_number)
    print("qwen3_30b_a3b_thinking_2507", len(qwen3_30b_a3b_thinking_2507) / total_number)

    print("relational filtering", len(samples_rational_filtering))
    total_number = len(samples_rational_filtering)
    qwen25_7b_instruct_1m_sft = []
    qwen25_7b_instruct_1m_grpo = []
    gemini25_pro = []
    gemma3_27b_it = []
    gpt41_20250414 = []
    llama33_70b_instruct = []
    llama4_scout_17b_16e_instruct = []
    o4mini_20250416 = []
    qwen25_14b_instruct_1m = []
    qwen25_7b_instruct_1m = []
    deepseek_r1_distill_llama_70b_instruct = []
    qwen3_4b_instruct_2507 = []
    qwen3_4b_thinking_2507 = []
    qwen3_30b_a3b_instruct_2507 = []
    qwen3_30b_a3b_thinking_2507 = []
    for sample in samples_rational_filtering:
        ground_truth_answer = sample["ground_truth_answer"]
        if sample["qwen25_7b_instruct_1m_sft"] == ground_truth_answer:
            qwen25_7b_instruct_1m_sft.append(1)
        if sample["qwen25_7b_instruct_1m_grpo"] == ground_truth_answer:
            qwen25_7b_instruct_1m_grpo.append(1)
        if sample["gemini25_pro"] == ground_truth_answer:
            gemini25_pro.append(1)
        if sample["gemma3_27b_it"] == ground_truth_answer:
            gemma3_27b_it.append(1)
        if sample["gpt41_20250414"] == ground_truth_answer:
            gpt41_20250414.append(1)
        if sample["llama33_70b_instruct"] == ground_truth_answer:
            llama33_70b_instruct.append(1)
        if sample["llama4_scout_17b_16e_instruct"] == ground_truth_answer:
            llama4_scout_17b_16e_instruct.append(1)
        if sample["o4mini_20250416"] == ground_truth_answer:
            o4mini_20250416.append(1)
        if sample["qwen25_14b_instruct_1m"] == ground_truth_answer:
            qwen25_14b_instruct_1m.append(1)
        if sample["qwen25_7b_instruct_1m"] == ground_truth_answer:
            qwen25_7b_instruct_1m.append(1)
        if sample["deepseek_r1_distill_llama_70b_instruct"] == ground_truth_answer:
            deepseek_r1_distill_llama_70b_instruct.append(1)
        if sample["qwen3_4b_instruct_2507"] == ground_truth_answer:
            qwen3_4b_instruct_2507.append(1)
        if sample["qwen3_4b_thinking_2507"] == ground_truth_answer:
            qwen3_4b_thinking_2507.append(1)
        if sample["qwen3_30b_a3b_instruct_2507"] == ground_truth_answer:
            qwen3_30b_a3b_instruct_2507.append(1)
        if sample["qwen3_30b_a3b_thinking_2507"] == ground_truth_answer:
            qwen3_30b_a3b_thinking_2507.append(1)
    print("qwen25_7b_instruct_1m_sft", len(qwen25_7b_instruct_1m_sft) / total_number)
    print("qwen25_7b_instruct_1m_grpo", len(qwen25_7b_instruct_1m_grpo) / total_number)
    print("gemini25_pro", len(gemini25_pro) / total_number)
    print("gemma3_27b_it", len(gemma3_27b_it) / total_number)
    print("gpt41_20250414", len(gpt41_20250414) / total_number)
    print("llama33_70b_instruct", len(llama33_70b_instruct) / total_number)
    print("llama4_scout_17b_16e_instruct", len(llama4_scout_17b_16e_instruct) / total_number)
    print("o4mini_20250416", len(o4mini_20250416) / total_number)
    print("qwen25_14b_instruct_1m", len(qwen25_14b_instruct_1m) / total_number)
    print("qwen25_7b_instruct_1m", len(qwen25_7b_instruct_1m) / total_number)
    print("deepseek_r1_distill_llama_70b_instruct", len(deepseek_r1_distill_llama_70b_instruct) / total_number)
    print("qwen3_4b_instruct_2507", len(qwen3_4b_instruct_2507) / total_number)
    print("qwen3_4b_thinking_2507", len(qwen3_4b_thinking_2507) / total_number)
    print("qwen3_30b_a3b_instruct_2507", len(qwen3_30b_a3b_instruct_2507) / total_number)
    print("qwen3_30b_a3b_thinking_2507", len(qwen3_30b_a3b_thinking_2507) / total_number)

    print("all",
          len(samples_rational_filtering + samples_filtering + samples_filtering_aggregating + samples_filtering_sorting))
    total_number = len(samples_rational_filtering + samples_filtering + samples_filtering_aggregating + samples_filtering_sorting)
    qwen25_7b_instruct_1m_sft = []
    qwen25_7b_instruct_1m_grpo = []
    gemini25_pro = []
    gemma3_27b_it = []
    gpt41_20250414 = []
    llama33_70b_instruct = []
    llama4_scout_17b_16e_instruct = []
    o4mini_20250416 = []
    qwen25_14b_instruct_1m = []
    qwen25_7b_instruct_1m = []
    deepseek_r1_distill_llama_70b_instruct = []
    qwen3_4b_instruct_2507 = []
    qwen3_4b_thinking_2507 = []
    qwen3_30b_a3b_instruct_2507 = []
    qwen3_30b_a3b_thinking_2507 = []
    for sample in samples_rational_filtering + samples_filtering + samples_filtering_aggregating + samples_filtering_sorting:
        ground_truth_answer = sample["ground_truth_answer"]
        if sample["qwen25_7b_instruct_1m_sft"] == ground_truth_answer:
            qwen25_7b_instruct_1m_sft.append(1)
        if sample["qwen25_7b_instruct_1m_grpo"] == ground_truth_answer:
            qwen25_7b_instruct_1m_grpo.append(1)
        if sample["gemini25_pro"] == ground_truth_answer:
            gemini25_pro.append(1)
        if sample["gemma3_27b_it"] == ground_truth_answer:
            gemma3_27b_it.append(1)
        if sample["gpt41_20250414"] == ground_truth_answer:
            gpt41_20250414.append(1)
        if sample["llama33_70b_instruct"] == ground_truth_answer:
            llama33_70b_instruct.append(1)
        if sample["llama4_scout_17b_16e_instruct"] == ground_truth_answer:
            llama4_scout_17b_16e_instruct.append(1)
        if sample["o4mini_20250416"] == ground_truth_answer:
            o4mini_20250416.append(1)
        if sample["qwen25_14b_instruct_1m"] == ground_truth_answer:
            qwen25_14b_instruct_1m.append(1)
        if sample["qwen25_7b_instruct_1m"] == ground_truth_answer:
            qwen25_7b_instruct_1m.append(1)
        if sample["deepseek_r1_distill_llama_70b_instruct"] == ground_truth_answer:
            deepseek_r1_distill_llama_70b_instruct.append(1)
        if sample["qwen3_4b_instruct_2507"] == ground_truth_answer:
            qwen3_4b_instruct_2507.append(1)
        if sample["qwen3_4b_thinking_2507"] == ground_truth_answer:
            qwen3_4b_thinking_2507.append(1)
        if sample["qwen3_30b_a3b_instruct_2507"] == ground_truth_answer:
            qwen3_30b_a3b_instruct_2507.append(1)
        if sample["qwen3_30b_a3b_thinking_2507"] == ground_truth_answer:
            qwen3_30b_a3b_thinking_2507.append(1)
    print(
          len(qwen3_4b_instruct_2507)/total_number, len(qwen3_4b_thinking_2507)/total_number, len(qwen3_30b_a3b_instruct_2507)/total_number,
          len(qwen3_30b_a3b_thinking_2507)/total_number)
    print("qwen25_7b_instruct_1m_sft", len(qwen25_7b_instruct_1m_sft)/total_number)
    print("qwen25_7b_instruct_1m_grpo", len(qwen25_7b_instruct_1m_grpo)/total_number)
    print("gemini25_pro", len(gemini25_pro)/total_number)
    print("gemma3_27b_it", len(gemma3_27b_it)/total_number)
    print("gpt41_20250414", len(gpt41_20250414)/total_number)
    print("llama33_70b_instruct", len(llama33_70b_instruct)/total_number)
    print("llama4_scout_17b_16e_instruct", len(llama4_scout_17b_16e_instruct)/total_number)
    print("o4mini_20250416", len(o4mini_20250416)/total_number)
    print("qwen25_14b_instruct_1m", len(qwen25_14b_instruct_1m)/total_number)
    print("qwen25_7b_instruct_1m", len(qwen25_7b_instruct_1m)/total_number)
    print("deepseek_r1_distill_llama_70b_instruct", len(deepseek_r1_distill_llama_70b_instruct)/total_number)
    print("qwen3_4b_instruct_2507", len(qwen3_4b_instruct_2507)/total_number)
    print("qwen3_4b_thinking_2507", len(qwen3_4b_thinking_2507)/total_number)
    print("qwen3_30b_a3b_instruct_2507", len(qwen3_30b_a3b_instruct_2507)/total_number)
    print("qwen3_30b_a3b_thinking_2507", len(qwen3_30b_a3b_thinking_2507)/total_number)