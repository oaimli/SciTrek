import pandas as pd
import json
import random
from google import genai
import os
from google.genai import types


if __name__ == "__main__":
    data = pd.read_excel("hard_for_all_128k.xlsx")
    questions = []
    combined = []
    for question, ground_truth, qwen25_7b_instruct_1m_sft, qwen25_7b_instruct_1m_grpo, gemini25_pro, gemma3_27b_it, gpt41_20250414, llama33_70b_instruct, llama4_scout_17b_16e_instruct, o4mini_20250416, qwen25_14b_instruct_1m, qwen25_7b_instruct_1m in zip(
            data["question"], data["answer"], data["qwen25_7b_instruct_1m_sft"], data["qwen25_7b_instruct_1m_grpo"],
            data["gemini25_pro"], data["gemma3_27b_it"], data["gpt41_20250414"], data["llama33_70b_instruct"],
            data["llama4_scout_17b_16e_instruct"], data["o4mini_20250416"], data["qwen25_14b_instruct_1m"],
            data["qwen25_7b_instruct_1m"]):
        questions.append(question)
        tmp = {}
        tmp["question"] = question
        tmp["ground_truth_answer"] = ground_truth
        model_answers = {}
        model_answers["qwen25_7b_instruct_1m_sft"] = qwen25_7b_instruct_1m_sft.split("\n")
        model_answers["qwen25_7b_instruct_1m_grpo"] = qwen25_7b_instruct_1m_grpo.split("\n")
        model_answers["gemini25_pro"] = gemini25_pro.split("\n")
        model_answers["gemma3_27b_it"] = gemma3_27b_it.split("\n")
        model_answers["gpt41_20250414"] = gpt41_20250414.split("\n")
        model_answers["llama33_70b_instruct"] = llama33_70b_instruct.split("\n")
        model_answers["llama4_scout_17b_16e_instruct"] = llama4_scout_17b_16e_instruct.split("\n")
        model_answers["o4mini_20250416"] = o4mini_20250416.split("\n")
        model_answers["qwen25_14b_instruct_1m"] = qwen25_14b_instruct_1m.split("\n")
        model_answers["qwen25_7b_instruct_1m"] = qwen25_7b_instruct_1m.split("\n")
        tmp["model_answers"] = model_answers
        combined.append(tmp)

    combined = random.sample(combined, 50)
    with open("model_answers.json", "w") as f:
        json.dump(combined, f, indent=4)


    model_name_official = "gemini-2.5-pro"
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    while True:
        try:
            instruction = open("instruction_fp.txt").read()
            prompt_content = instruction.replace("<data>", open("model_answers.json").read())
            response = client.models.generate_content(
                model=model_name_official,
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=512, include_thoughts=False),
                    candidate_count=1
                    ),
                )
            # print(response.candidates)
            generations = []
            for candidate in response.candidates:
                generations.append(candidate.content.parts[0].text)
                print(candidate.content.parts[0].text)
            break
        except Exception as e:
            print(e)
