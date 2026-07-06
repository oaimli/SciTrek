import os
import re
import string
from nltk.metrics import f_measure
from rouge_score import rouge_scorer
import jsonlines
import numpy as np
import pandas as pd
import json
from collections import Counter
from scipy import stats


def normalize_text(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match(generation_batches, references):
    ems = []
    for generation_batch, reference in zip(generation_batches, references):
        ems_batch = []
        for generation in generation_batch:
            normalized_generation = normalize_text(generation)
            normalized_reference = normalize_text(reference)
            if normalized_generation == normalized_reference:
                ems_batch.append(1)
            else:
                ems_batch.append(0)
        ems.append(np.average(ems_batch))
    return {'em': ems}


def f1_score(generation_batches, references):
    f1_scores = []
    for generation_batch, reference in zip(generation_batches, references):
        f1_scores_batch = []
        for generation in generation_batch:
            score = f_measure(
                set(normalize_text(reference).split()), set(normalize_text(generation).split())
                )
            if score is None:  # answer is the empty string after normalizing
                score = 0.0
            f1_scores_batch.append(score)
        f1_scores.append(np.average(f1_scores_batch))
    return {"f1": f1_scores}


def rouge_l(generation_batches, references):
    scores = []
    for generation_batch, reference in zip(generation_batches, references):
        scores_batch = []
        for generation in generation_batch:
            scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
            eval = scorer.score(reference, generation)
            score = eval["rougeL"].fmeasure
            scores_batch.append(score)
        scores.append(np.average(scores_batch))

    return {"rouge-l": scores}


def evaluating(generation_batches, references):
    # preprocessing
    generation_batches_processed = []
    for generation_batch in generation_batches:
        generation_batch_processed = []
        for generation in generation_batch:
            # the generated answer may be a list
            generation = str(generation)

            generation = generation.strip()
            generation = " ".join(generation.split())
            generation = ", ".join([tmp.strip() for tmp in generation.split(",")])
            generation_batch_processed.append(generation)
        generation_batches_processed.append(generation_batch_processed)

    scores = {}
    scores.update(exact_match(generation_batches_processed, references))
    scores.update(f1_score(generation_batches_processed, references))
    scores.update(rouge_l(generation_batches_processed, references))

    return scores


if __name__ == "__main__":
    with open(os.path.join("../../bench/article/", "papers_final.json")) as f:
        articles_all = json.load(f)

    models = set([])
    unfinished = set([])
    for generation_result in os.listdir("../../results_test/"):
        if generation_result.endswith(".jsonl") and "test_full" in generation_result and "128k" in generation_result:
            tmp = []

            models.add("_".join(generation_result.split(".")[0].split("_")[3:]))
            with jsonlines.open(os.path.join("../../results_test/", f"{generation_result}")) as reader:
                for line in reader:
                    if "generations" in line.keys():
                        tmp.append(line)
                    else:
                        unfinished.add(generation_result)
            print(generation_result, len(tmp))

    print("models", models, unfinished)
    models = list(models)
    models.append("qwen-grpo")
    models.append("qwen-sft")
    models.sort()

    all_results = {}
    for model in models:
        print(f"Evaluating model {model}")
        model_results = {}

        answers = []
        generation_batches = []
        input_lengths = []
        document_counts = []
        question_lengths = []
        sql_lengths = []
        answer_lengths = []
        ems = []
        rls = []
        f1s = []
        if model == "qwen-grpo":
            result_folder = "../../train_grpo/grpo/generations_sampled_192"
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(
                        ".jsonl") and "test_full" in generation_result and "128k" in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                                answers.append(line["answer"])
                                generation_batches.append(line["generations"])
                                sql_lengths.append(len(line["sql"].split()))
                                question_lengths.append(len(line["question"].split()))
                                answer_lengths.append(len(line["answer"].split()))

                                input_lengths_tmp = []
                                for article_id in line["articles"]:
                                    article_details = articles_all[article_id]
                                    subtopic = article_details["subtopic"]
                                    input_lengths_tmp.append(len(article_details["markdown"].split()))
                                input_lengths.append(sum(input_lengths_tmp))
                                document_counts.append(len(line["articles"]))
        elif model == "qwen-sft":
            result_folder = "../../train_sft/input_length/generations"
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(
                        ".jsonl") and "test_full" in generation_result and "128k" in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                                answers.append(line["answer"])
                                generation_batches.append(line["generations"])
                                sql_lengths.append(len(line["sql"].split()))
                                question_lengths.append(len(line["question"].split()))
                                answer_lengths.append(len(line["answer"].split()))

                                input_lengths_tmp = []
                                for article_id in line["articles"]:
                                    article_details = articles_all[article_id]
                                    subtopic = article_details["subtopic"]
                                    input_lengths_tmp.append(len(article_details["markdown"].split()))
                                input_lengths.append(sum(input_lengths_tmp))
                                document_counts.append(len(line["articles"]))
        else:
            result_folder = "../../results_test/"
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(".jsonl") and "test_full" in generation_result and "128k" in generation_result and model in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                                answers.append(line["answer"])
                                generation_batches.append(line["generations"])
                                sql_lengths.append(len(line["sql"].split()))
                                question_lengths.append(len(line["question"].split()))
                                answer_lengths.append(len(line["answer"].split()))

                                input_lengths_tmp = []
                                for article_id in line["articles"]:
                                    article_details = articles_all[article_id]
                                    subtopic = article_details["subtopic"]
                                    input_lengths_tmp.append(len(article_details["markdown"].split()))
                                input_lengths.append(sum(input_lengths_tmp))
                                document_counts.append(len(line["articles"]))

        print(len(generation_batches), len(answers))
        scores = evaluating(generation_batches, answers)
        for metric, values_tmp in scores.items():
            if metric == "em":
                ems = values_tmp
            if metric == "rouge-l":
                rls = values_tmp
            if metric == "f1":
                f1s = values_tmp

        def cal_corr(scores, features):
            tmp = stats.pearsonr(features, scores)
            print(tmp)
            corr = round(tmp[0], 5)
            pvalue = round(tmp[1], 5)
            return corr, pvalue


        # # input length
        # print("input length")
        # print(input_lengths)
        # # for i, item_tmp in enumerate(input_lengths):
        # #     input_lengths[i] = item_tmp / max(input_lengths)
        # corr, pvalue = cal_corr(ems, input_lengths)
        # model_results["input_length"] = f"{corr}/{pvalue}"

        print("document count")
        # document count
        # print(document_counts)
        # for i, item_tmp in enumerate(document_counts):
        #     document_counts[i] = item_tmp / max(document_counts)
        corr, pvalue = cal_corr(ems, document_counts)
        model_results["document_count"] = f"{corr}/{pvalue}"

        # question lengths
        print("question length")
        # print(question_lengths)
        # for i, item_tmp in enumerate(question_lengths):
        #     question_lengths[i] = item_tmp / max(question_lengths)
        corr, pvalue = cal_corr(ems, question_lengths)
        model_results["question_length"] = f"{corr}/{pvalue}"

        # sql lengths
        print("sql length")
        # print(sql_lengths)
        # for i, item_tmp in enumerate(sql_lengths):
        #     sql_lengths[i] = item_tmp / max(sql_lengths)
        corr, pvalue = cal_corr(ems, sql_lengths)
        model_results["sql_length"] = f"{corr}/{pvalue}"

        # answer lengths
        print("answer length")
        # print(answer_lengths)
        # for i, item_tmp in enumerate(answer_lengths):
        #     answer_lengths[i] = item_tmp / max(answer_lengths)
        corr, pvalue = cal_corr(ems, answer_lengths)
        model_results["answer_length"] = f"{corr}/{pvalue}"

        all_results[model] = model_results

    # output excel
    df = pd.DataFrame.from_dict(all_results, orient="columns")
    df.index.name = "column"
    df.to_excel("difficulty_128k_em.xlsx", sheet_name="more")

