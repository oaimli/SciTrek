import jsonlines
import os

if __name__ == "__main__":
    # loading test data, one level of samples at each time
    sqls_test = []
    for prefix in ["single", "64k", "128k", "512k", "1024k"]:

        sqls_test_tmp = []
        save_file = os.path.join("../bench/dataset/samples/final/", f"{prefix}_samples_target.jsonl")
        with jsonlines.open(save_file) as reader:
            for line in reader:
                valid_sample = True
                if line["question"] == "":
                    valid_sample = False
                if "database" in line["question"]:
                    valid_sample = False

                if valid_sample:
                    if line["label"] == "test":
                        sqls_test_tmp.append(line["sql"])
        print(prefix, len(sqls_test_tmp))
        sqls_test.extend(sqls_test_tmp)

    print(len(sqls_test), len(set(sqls_test)))
    sqls_test = list(set(sqls_test))
    with jsonlines.open("sqls_test.jsonl", mode="w") as writer:
        writer.write_all(sqls_test)

    # single 122
    # 64k 143
    # 128k 883
    # 512k 772
    # 1024k 705
    # 2625 1295