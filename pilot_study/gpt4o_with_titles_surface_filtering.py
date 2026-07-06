# prompting with no contexts for question answering
import os
import time
from openai import OpenAI
from tqdm import tqdm
import random
import sys

sys.path.append("../")
from utils.tokenizer_llama3.tokenizer import Tokenizer


if __name__ == "__main__":
    client = OpenAI(api_key="")

    window_size = 128*1024
    max_context = window_size - 1024
    max_papers = 5

    # load all source articles
    papers_md = []
    loong_papers_dir = "data"
    for filename in tqdm(os.listdir(loong_papers_dir)):
        if filename.endswith(".md"):
            with open(os.path.join(loong_papers_dir, filename), "r") as f:
                papers_md.append({"file_name": filename, "content": f.read()})
    print("Loong papers: {}".format(len(papers_md)))

    # select articles as the context
    random.seed(42)
    random.shuffle(papers_md)
    tokenizer = Tokenizer("../utils/tokenizer_llama3/tokenizer.model")

    filenames_selected = []
    contents_selected = []
    max_length = 0
    for paper in papers_md:
        filename = paper["file_name"]
        content = paper["content"]
        paper_length = len(tokenizer.encode(content, bos=True, eos=True))
        if max_length + paper_length <= window_size and len(filenames_selected) < max_papers:
            filenames_selected.append(filename)
            contents_selected.append(content)
            max_length = max_length + paper_length
        else:
            break
    filenames_selected = ['1709.03082.md', '1508.01745.md', '1604.05377.md', '1610.04325.md', '1803.08375.md']
    print("selected papers: ", filenames_selected)

    for filename, content in zip(filenames_selected, contents_selected):
        instruction = "Tell me how many references the give paper has. Only output the number of references."
        prompt_content = f"{content}\n\n{instruction}"
        while True:
            try:
                output_dict = client.chat.completions.create(
                    model="gpt-4o-2024-11-20",
                    messages=[
                        {"role": "system",
                         "content": "You are requested to give response to the instruction, without any not useful content."},
                        {"role": "user",
                         "content": prompt_content}
                    ],
                    n=1
                )
                output = output_dict.choices[0].message.content
                break
            except Exception as e:
                print(e)
                if "limit" in str(e):
                    time.sleep(2)
        print(filename, output)

    papers_md_context = "\n\n".join(contents_selected)
    print("Length of input", max_length)


    instruction = "Tell me the papers that have more than 30 references.\n You must only output the titles of the papers following the format below:\npaper-1\npaper-2\n...\npaper-n"
    print(instruction)
    prompt_content = f"{papers_md_context}\n\n{instruction}"
    with open("example_with_titles_surface_filtering.txt", "w") as f:
        f.write(prompt_content)
    while True:
        try:
            output_dict = client.chat.completions.create(
                model="gpt-4o-2024-11-20",
                messages=[
                    {"role": "system",
                     "content": "You are requested to give response to the instruction, without any not useful content."},
                    {"role": "user",
                     "content": prompt_content}
                ],
                n=1
            )
            output = output_dict.choices[0].message.content
            break
        except Exception as e:
            print(e)
            if "limit" in str(e):
                time.sleep(2)
    print(output)

