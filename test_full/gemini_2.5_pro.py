import time
from tqdm import tqdm
import os
import sys
import jsonlines
from google import genai
from google.genai import types


sys.path.append("../")
from benchmark.dataset.data_loading import load_test, load_articles, get_full_texts

if __name__ == "__main__":
    model_name_official = "gemini-2.5-pro"
    target_mode = "test_full"
    model_name_save = "gemini25_pro"
    sample_level = "512k"

    articles_all = load_articles(articles_folder="../benchmark/article/")

    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    save_name = f"../results_test/{sample_level}_{target_mode}_{model_name_save}.jsonl"
    if os.path.exists(save_name):
        samples_test = []
        with jsonlines.open(save_name) as reader:
            for line in reader:
                samples_test.append(line)
        print("existing results loaded", len(samples_test))
    else:
        samples_test = load_test(prefix=sample_level, samples_folder="../benchmark/dataset/samples/final/")
        print("original samples loaded", len(samples_test))

    for sample_index, sample in tqdm(enumerate(samples_test), total=len(samples_test), desc=f"{model_name_save}_{sample_level}"):
        if "generations" not in sample.keys():
            while True:
                try:
                    question = sample["question"]
                    markdowns = get_full_texts(sample, articles_all)

                    context = "\n".join(markdowns)
                    instruction = open("../benchmark/dataset/instructions/instruction_full_scitrek.txt").read()
                    instruction = instruction.replace("<question>", question)
                    prompt_content = instruction.replace("<articles>", context)
                    response = client.models.generate_content(
                        model=model_name_official,
                        contents=prompt_content,
                        config=types.GenerateContentConfig(
                            thinking_config=types.ThinkingConfig(thinking_budget=512, include_thoughts=False),
                            candidate_count=3
                            ),
                        )
                    generations = []
                    for candidate in response.candidates:
                        generations.append(candidate.content.parts[0].text)
                    print("original answer", sample["answer"])
                    print("generated result", generations)
                    sample["generations"] = generations
                    break
                except Exception as e:
                    print(e)
                    time.sleep(2)

            samples_test[sample_index] = sample
            with jsonlines.open(save_name, "w") as writer:
                writer.write_all(samples_test)

    with jsonlines.open(save_name, "w") as writer:
        writer.write_all(samples_test)