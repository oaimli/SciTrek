import jsonlines
import random
import json


# load valid data
random.seed(42)
samples_all = []
for prefix in ["64k", "128k", "512k", "1024k", "single"]:
    save_file = f"../../dataset/samples/final/{prefix}_samples_target.jsonl"

    samples_tmp = []
    with jsonlines.open(save_file) as reader:
        for line in reader:
            if line["question"] != "" and "database" not in line["question"]:
                samples_tmp.append(line)
    samples_all.extend(samples_tmp)
print("samples all", len(samples_all))

detailed_samples = {}
for sample in samples_all:
    if sample["question"] != "":
        info = sample["sql_type"]
        tmp = detailed_samples.get(info, [])
        tmp.append(sample)
        detailed_samples[info] = tmp
print("SQL categories", len(detailed_samples))
sampled_samples = []
for info, samples_tmp in detailed_samples.items():
    templates = set([])
    for sample in samples_all:
        if sample["sql_type"] == info and sample["question"] != "":
            template = sample["template"]
            templates.add(template)
    print(info, "samples:", len(samples_tmp), "templates:", len(templates))

    sampled_samples.extend(random.sample(samples_tmp, 30))
random.shuffle(sampled_samples)
with open("sampled_samples.json", "w") as f:
    json.dump(sampled_samples, f, indent=4)
