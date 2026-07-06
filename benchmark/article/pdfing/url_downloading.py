# download the pdfs with the urls in paper details
import json
import os.path
from tqdm import tqdm
import time
from requests import Session
import random

with open("../graphs.json") as f:
    graphs = json.load(f)

papers_detail = []
for subtopic, graph in graphs.items():
    print(subtopic)
    for paper_id, paper_details in graph.items():
        pdf_access = paper_details["pdf_access"]
        pdf_url = ""
        if pdf_access != None:
            if "url" in paper_details.keys():
                pdf_url = pdf_access["url"]
        papers_detail.append({"paper_id": paper_id, "pdf_url": pdf_url, "subtopic": subtopic})
print("all papers", len(papers_detail))
random.seed(42)
random.shuffle(papers_detail)

index = 0
for item in tqdm(papers_detail[0:]):
    paper_id = item["paper_id"]
    pdf_url = item["pdf_url"]
    subtopic = item["subtopic"]
    print(f"downloading {index}", paper_id, "from", pdf_url)
    os.makedirs(f"../../pdfs/", exist_ok=True)
    index += 1
    if pdf_url.strip() == "":
        continue
    saved_path = f"../../pdfs/{paper_id}.pdf"
    if not os.path.exists(saved_path):
        with Session() as session:
            # send a user-agent to avoid server error
            headers = {'user-agent': 'requests/2.0.0'}
            # stream the response to avoid downloading the entire file into memory
            with session.get(pdf_url, headers=headers, stream=True, verify=False) as response:
                # check if the request was successful
                if response.status_code == 200:
                    if response.headers['content-type'] != 'application/pdf':
                        continue

                    with open(saved_path, 'wb') as f:
                        # write the response to the file, chunk_size bytes at a time
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded {paper_id} to {saved_path}")
                else:
                    print("Error", response.status_code)
                time.sleep(5)
    else:
        print(f"Existed {paper_id} to {saved_path}")