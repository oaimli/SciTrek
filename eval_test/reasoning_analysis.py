import jsonlines
import numpy as np


samples_deepseek_r1 = []
with jsonlines.open("../results_test/64k_test_full_deepseek_r1_distill_llama_70b_instruct.jsonl") as reader:
    for line in reader:
        samples_deepseek_r1.append(line)
with jsonlines.open("../results_test/128k_test_full_deepseek_r1_distill_llama_70b_instruct.jsonl") as reader:
    for line in reader:
        samples_deepseek_r1.append(line)

reasoning_traces = []
for sample in samples_deepseek_r1:
    reasonings = sample["reasonings"]
    for reasoning in reasonings:
        reasoning_traces.append(len(reasoning.split()))
print(np.mean(reasoning_traces), len(reasoning_traces)/3)


samples_qwen3_4b_thinking = []
with jsonlines.open("../results_test/64k_test_full_qwen3_4b_thinking_2507.jsonl") as reader:
    for line in reader:
        samples_qwen3_4b_thinking.append(line)
with jsonlines.open("../results_test/128k_test_full_qwen3_4b_thinking_2507.jsonl") as reader:
    for line in reader:
        samples_qwen3_4b_thinking.append(line)

reasoning_traces = []
for sample in samples_qwen3_4b_thinking:
    reasonings = sample["reasonings"]
    for reasoning in reasonings:
        reasoning_traces.append(len(reasoning.split()))
print(np.mean(reasoning_traces), len(reasoning_traces)/3)