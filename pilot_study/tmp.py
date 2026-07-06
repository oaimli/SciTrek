import os
from tqdm import tqdm
import sys
import numpy as np

sys.path.append("../")
from dl_reasoning.construction.llama3_tokenizer.tokenizer import Tokenizer


if __name__ == "__main__":
    # load all source articles
    papers_md = []
    loong_papers_dir = "../sources/loong"
    for filename in tqdm(os.listdir(loong_papers_dir)):
        if filename.endswith(".md"):
            with open(os.path.join(loong_papers_dir, filename), "r") as f:
                papers_md.append({"file_name": filename, "content": f.read()})
    print("Loong papers: {}".format(len(papers_md)))

    tokenizer = Tokenizer("../construction/llama3_tokenizer/tokenizer.model")

    paper_lengths = []
    for paper in papers_md:
        filename = paper["file_name"]
        content = paper["content"]
        paper_length = len(tokenizer.encode(content, bos=True, eos=True))
        paper_lengths.append(paper_length)

    print("The average paper length: {}".format(np.mean(paper_lengths)))