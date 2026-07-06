import jsonlines

data_folder = "/Users/miao4/Workspace/crawled/multi-document/Loong-main/data"
samples = []
with jsonlines.open(f"{data_folder}/loong.jsonl") as reader:
    for line in reader:
        samples.append(line)

samples_selected = []
instructions_questions = []
for sample in samples:
    if sample["type"] == "paper":
        instructions_questions.append(sample["instruction"] + "\n" + sample["question"])
        samples_selected.append(sample)

print(len(samples_selected))
print(len(set(instructions_questions)))
instructions_questions = list(set(instructions_questions))
with jsonlines.open("questions_loong.jsonl", "w") as writer:
    writer.write_all(instructions_questions)
