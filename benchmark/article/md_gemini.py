import json
import random
from tqdm import tqdm
from google import genai
from google.genai import types
import pathlib
import time
import os


client = genai.Client(api_key="AIzaSyDKp-y37Bld0PfiRzGMxXimj9nTMwhkNxg")

with open("papers_annotated.json") as f:
    papers_annotated = json.load(f)

markdown_folder = "../md_gemini/"
pdf_folder = "../pdfs"
paper_ids = list(papers_annotated.keys())
random.shuffle(paper_ids)

papers_processing = []
for paper_id in paper_ids:
    md_file = os.path.join(markdown_folder, paper_id + ".md")
    if not os.path.exists(md_file):
        papers_processing.append(paper_id)

for paper_id in tqdm(papers_processing):
    md_file = os.path.join(markdown_folder, paper_id + ".md")
    pdf_file = os.path.join(pdf_folder, paper_id + ".pdf")
    print(paper_id)
    try:
        # Retrieve and encode the PDF byte
        filepath = pathlib.Path(pdf_file)
        prompt = open("prompt_md.txt").read().strip()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=filepath.read_bytes(),
                    mime_type='application/pdf',
                    ),
                prompt])
        with open(md_file, "w") as f:
            f.write(response.text)
        time.sleep(10)
    except Exception as e:
        print(e)



