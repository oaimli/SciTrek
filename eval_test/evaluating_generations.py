import os
import re
import string
from nltk.metrics import f_measure
import jsonlines
import numpy as np


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
        if len(generation_batch) <= 3:
            ems_batch = []
            for generation in generation_batch:
                normalized_generation = normalize_text(generation)
                normalized_reference = normalize_text(reference)
                if normalized_generation == normalized_reference:
                    ems_batch.append(1)
                else:
                    ems_batch.append(0)
            ems.append(np.average(ems_batch))
        else:
            assert len(generation_batch) % 3 == 0
            ems_batch = []
            tmp = []
            for generation in generation_batch:
                normalized_generation = normalize_text(generation)
                normalized_reference = normalize_text(reference)
                if normalized_generation == normalized_reference:
                    tmp.append(1)
                else:
                    tmp.append(0)
                if len(tmp) == 3:
                    ems_batch.append(np.average(tmp))
                    tmp = []
            ems.append(np.max(ems_batch))
    return {'em': ems}


def f1_score(generation_batches, references):
    f1_scores = []
    for generation_batch, reference in zip(generation_batches, references):
        if len(generation_batch) <= 3:
            f1_scores_batch = []
            for generation in generation_batch:
                score = f_measure(
                    set(normalize_text(reference).split()), set(normalize_text(generation).split())
                    )
                if score is None:  # answer is the empty string after normalizing
                    score = 0.0
                f1_scores_batch.append(score)
            f1_scores.append(np.average(f1_scores_batch))
        else:
            assert len(generation_batch) % 3 == 0
            f1_scores_batch = []
            tmp = []
            for generation in generation_batch:
                score = f_measure(
                    set(normalize_text(reference).split()), set(normalize_text(generation).split())
                    )
                if score is None:  # answer is the empty string after normalizing
                    score = 0.0
                tmp.append(score)
                if len(tmp) == 3:
                    f1_scores_batch.append(np.average(tmp))
                    tmp = []
            f1_scores.append(np.max(f1_scores_batch))
    return {"f1": f1_scores}


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

    return scores


if __name__ == "__main__":
    result_folder = "../results_test/"

    # comparing models in different sample_level and target_mode
    output_files = []
    for generation_result in os.listdir(result_folder):
        if generation_result.endswith(".jsonl") and "qwen25_coder" in generation_result:
            output_files.append(generation_result)
    output_files.sort()

    for generation_file in output_files:

        answers = []
        generation_batches = []
        with jsonlines.open(os.path.join(result_folder, f"{generation_file}")) as reader:
            for line in reader:
                if "generations" in line.keys() and line["answer"] != "NULL" and line["sql_type"] != "multi_simple":
                    answers.append(line["answer"])
                    generation_batches.append(line["generations"])
                    # print(line["answer"], line["generations"])
        print(generation_file, len(generation_batches), len(answers))
        scores = evaluating(generation_batches, answers)
        metrics = []
        values_all = []
        for metric, values_tmp in scores.items():
            metrics.append(metric)
            values_all.append(str(round(np.mean(values_tmp), 3)))
        print(metrics, "/".join(values_all))