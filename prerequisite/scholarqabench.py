import jsonlines


scholarqa_samples = []
with jsonlines.open("scholarqabench.jsonl") as reader:
    for line in reader:
        scholarqa_samples.append(line["input"])
print(len(scholarqa_samples))
# with jsonlines.open("questions.jsonl", "w") as writer:
#     writer.write_all(longbench_samples + scholarqa_samples)

scholarqa_samples = []
with jsonlines.open("scholarqabench.jsonl") as reader:
    for line in reader:
        scholarqa_samples.append(line["input"])
print(len(scholarqa_samples))
with jsonlines.open("questions_scholarqabench.jsonl", "w") as writer:
    writer.write_all(scholarqa_samples)

