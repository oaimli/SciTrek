import sys
import json

sys.path.append("../../")
from bench.dataset.data_loading import load_test, load_train


if __name__ == "__main__":
    train_data, dev_data = load_train(prefixes=["128k"], samples_folder="../../bench/dataset/samples/final/", no_null=True)
    test_data = load_test(prefix="128k", samples_folder="../../bench/dataset/samples/final", no_null=True)

    examples = []
    questions = set([])
    for sample in train_data + dev_data + test_data:
        question = sample["question"]
        sql_query = sample["sql"]
        answer = sample["answer"]
        if question not in questions:
            questions.add(question)
            tmp = {}
            tmp["question"] = question
            tmp["sql_query"] = sql_query
            tmp["answer"] = answer
            tmp["sql_type"] = sample["sql_type"]
            tmp["question_focus"] = sample["focus"]
            examples.append(tmp)

    print("examples:", len(examples))
    with open("example_questions.json", "w") as f:
        json.dump(examples, f, indent=4)