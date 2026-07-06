import jsonlines


longbench_samples = []
with jsonlines.open("longbench_v2.jsonl") as reader:
    for line in reader:
        longbench_samples.append(line["question"])
print(len(longbench_samples))
domains = set([])
sub_domains = set()
academic_questions = set()
for sample in longbench_samples:
    domains.add(sample["domain"])
    sub_domains.add(sample["sub_domain"])
    if sample["sub_domain"] == "Academic":
        academic_questions.add(sample["question"])
print(domains)
print(sub_domains)
print("unique academic questions:", len(academic_questions))
print(academic_questions)

with jsonlines.open("questions_longbench_v2.jsonl", "w") as writer:
    writer.write_all(longbench_samples)

