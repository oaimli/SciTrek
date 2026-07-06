# downloading pdfs with crawling the webpages of semantic scholar reader
import time
import urllib.request
import json
import os
import wget
from tqdm import tqdm

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

existing_pdfs = 0
for item in papers_detail:
    paper_id = item["paper_id"]
    cluster = []
    for tmp in os.listdir(f"../../pdfs/"):
        if tmp.endswith(".pdf"):
            cluster.append(tmp)
    if f"{paper_id}.pdf" in cluster:
        existing_pdfs += 1
    else:
        print(f"https://www.semanticscholar.org/reader/{paper_id}")
print("existing paper count", existing_pdfs)

for item in tqdm(papers_detail):
    paper_id = item["paper_id"]
    pdf_url = item["pdf_url"]
    subtopic = item["subtopic"]
    os.makedirs(f"../../pdfs/", exist_ok=True)
    saved_path = f"../../pdfs/{paper_id}.pdf"
    if not os.path.exists(saved_path):
        print("downloading", paper_id, subtopic)
        url = f"https://www.semanticscholar.org/reader/{paper_id}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = str(response.read())
        print("reader url", f"https://www.semanticscholar.org/reader/{paper_id}")
        start = html.find("https://export.arxiv.org")
        end = html.find(".pdf", start)
        print(start, end, html[start:end] + ".pdf")

        if start != -1 and end != -1:
            wget.download(html[start:end] + ".pdf", saved_path)
            time.sleep(5)
            print("downloaded")
        else:
            print("failed")

        # print("downloading", paper_id, subtopic)
        # url = f"https://www.semanticscholar.org/reader/{paper_id}"
        # req = urllib.request.Request(url)
        # response = urllib.request.urlopen(req)
        # html = str(response.read())
        # print("reader url", f"https://www.semanticscholar.org/reader/{paper_id}")
        # if len(html) > 100:
        #     start = html.find("https://pdfs.semanticscholar.org/")
        #     end = html.find(".pdf", start)
        #     print(start, end, html[start:end] + ".pdf")
        #
        #     if start != -1 and end != -1:
        #         wget.download(html[start:end] + ".pdf", saved_path_extra)
        #         time.sleep(5)
        #         print("downloaded")
        #     else:
        #         print("failed")

        # print("downloading", paper_id, subtopic)
        # url = f"https://www.semanticscholar.org/paper/{paper_id}"
        # req = urllib.request.Request(url)
        # response = urllib.request.urlopen(req)
        # html = str(response.read())
        # print("reader url", url)
        # if len(html) > 100:
        #     start = html.find("https://pdfs.semanticscholar.org/")
        #     end = html.find(".pdf", start)
        #     print(start, end, html[start:end] + ".pdf")
        #
        #     if start != -1 and end != -1:
        #         wget.download(html[start:end] + ".pdf", saved_path)
        #         time.sleep(5)
        #         print("downloaded")
        #     else:
        #         print("failed")
        #     break