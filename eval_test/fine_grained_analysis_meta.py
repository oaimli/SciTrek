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
    result_folder = "../results_test/"

    with open(os.path.join("../bench/article/", "papers_final.json")) as f:
        articles_all = json.load(f)

    sql_types = set([])
    test_focuses = set([])
    question_complexities = set([])
    models = set([])
    unfinished = set([])
    domains = set([])
    for generation_result in os.listdir(result_folder):
        if generation_result.endswith(".jsonl") and "test_meta" in generation_result:
            tmp = []

            models.add("_".join(generation_result.split(".")[0].split("_")[3:]))
            with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                for line in reader:
                    if "generations" in line.keys():
                        sql_type = line["sql_type"]
                        sql_types.add(sql_type)
                        test_focus = line["focus"]
                        test_focuses.add(test_focus)
                        question_complexity = len(line["sql"].split())
                        question_complexities.add(question_complexity)
                        tmp.append(line)

                        for article_id in line["articles"]:
                            article_details = articles_all[article_id]
                            subtopic = article_details["subtopic"]
                            domains.add(subtopic)
                    else:
                        unfinished.add(generation_result)
            print(generation_result, len(tmp))

    print("sql_types", sql_types)
    print("question_focuses", test_focuses)
    print("models", models, unfinished)
    print("domains", domains)
    sql_types = list(sql_types)
    sql_types.sort()
    test_focuses = list(test_focuses)
    test_focuses.sort()
    models = list(models)
    models.sort()
    domains = list(domains)
    domains.sort()
    sql_types = ["multi_graph_filtering", "multi_ran_aggregating", "multi_ran_filtering_foa", "multi_ran_filtering_foo", "multi_ran_filtering_ofo", "multi_ran_organizing"]
    domains = ["computer_science", "economics", "electronic_engineering", "mathematics", "physics", "biology", "finance", "statistics"]

    # without samples that have "NULL" answers
    all_results = {}
    em_results = {}
    f1_results = {}
    rouge_l_results = {}
    for model in models:
        print(f"Evaluating model {model}")
        model_results_all = {}
        model_results_em = {}
        model_results_f1 = {}
        model_results_rouge_l = {}

        # question focus
        for test_focus in test_focuses:
            print(f"Testing focus {test_focus}")
            answers = []
            generation_batches = []
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(".jsonl") and "test_meta" in generation_result and model in generation_result and "128k" in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["focus"] == test_focus and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                                answers.append(line["answer"])
                                generation_batches.append(line["generations"])
            print(len(generation_batches), len(answers))
            scores = evaluating(generation_batches, answers)
            metrics = []
            values_all = []
            for metric, values_tmp in scores.items():
                metrics.append(metric)
                values_all.append(str(round(np.mean(values_tmp), 3)))
            print(metrics, "/".join(values_all))
            model_results_all[test_focus] = "/".join(values_all)
            model_results_em[test_focus] = values_all[0]
            model_results_f1[test_focus] = values_all[1]
            model_results_rouge_l[test_focus] = values_all[2]

        # sql type
        for sql_type in sql_types:
            print(f"Evaluating sql type {sql_type}")
            answers = []
            generation_batches = []
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(".jsonl")and "test_meta" in generation_result  and model in generation_result and "128k" in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["sql_type"] == sql_type and line["answer"] != "NULL":
                                answers.append(line["answer"])
                                generation_batches.append(line["generations"])
            print(len(generation_batches), len(answers))
            scores = evaluating(generation_batches, answers)
            metrics = []
            values_all = []
            for metric, values_tmp in scores.items():
                metrics.append(metric)
                values_all.append(str(round(np.mean(values_tmp), 3)))
            print(metrics, "/".join(values_all))
            model_results_all[sql_type] = "/".join(values_all)
            model_results_em[sql_type] = values_all[0]
            model_results_f1[sql_type] = values_all[1]
            model_results_rouge_l[sql_type] = values_all[2]

        # domain
        for domain in domains:
            print(f"Evaluating domain {domain}")
            answers = []
            generation_batches = []
            for generation_result in os.listdir(result_folder):
                if generation_result.endswith(
                        ".jsonl") and "test_meta" in generation_result and model in generation_result and "128k" in generation_result:
                    with jsonlines.open(os.path.join(result_folder, f"{generation_result}")) as reader:
                        for line in reader:
                            if "generations" in line.keys() and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                                subtopics = []
                                for article_id in line["articles"]:
                                    article_details = articles_all[article_id]
                                    subtopic = article_details["subtopic"]
                                    subtopics.append(subtopic)
                                domain_tmp = Counter(subtopics).most_common(1)[0][0]
                                if domain in domain_tmp:
                                    answers.append(line["answer"])
                                    generation_batches.append(line["generations"])
            print(len(generation_batches), len(answers))
            scores = evaluating(generation_batches, answers)
            metrics = []
            values_all = []
            for metric, values_tmp in scores.items():
                metrics.append(metric)
                values_all.append(str(round(np.mean(values_tmp), 3)))
            print(metrics, "/".join(values_all))
            model_results_all[domain] = "/".join(values_all)
            model_results_em[domain] = values_all[0]
            model_results_f1[domain] = values_all[1]
            model_results_rouge_l[domain] = values_all[2]

        all_results[model] = model_results_all
        em_results[model] = model_results_em
        f1_results[model] = model_results_f1
        rouge_l_results[model] = model_results_rouge_l

        print(len(model_results_em.keys()), len(model_results_f1.keys()), len(model_results_rouge_l.keys()))
    # output json
    with open("fine_grained_filtering_128k_em_meta.json", mode="w") as f:
        json.dump(em_results, f)
    with open("fine_grained_filtering_128k_f1_meta.json", mode="w") as f:
        json.dump(f1_results, f)
    with open("fine_grained_filtering_128k_rouge_l_meta.json", mode="w") as f:
        json.dump(rouge_l_results, f)

    # output excel
    df = pd.DataFrame.from_dict(all_results, orient="columns")
    df.index.name = "row"
    df.to_excel("fine_grained_filtering_128k_meta.xlsx", sheet_name="more")

