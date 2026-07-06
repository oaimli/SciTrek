# Use Gemini to correct the metainfo in papers_annotated.json
import json
import random

from google import genai
from google.genai import types
import pathlib
import time
import os


client = genai.Client(api_key="AIzaSyDKp-y37Bld0PfiRzGMxXimj9nTMwhkNxg")

# # calculate the accuracy of the annotation with human annotated samples
# with open("papers_annotated.json") as f:
#     papers_annotated = json.load(f)
#
# pdf_folder = "../pdfs"
# paper_ids = list(papers_annotated.keys())
# random.shuffle(paper_ids)
#
# results_authors = []
# results_titles = []
# results_references = []
# for paper_id in paper_ids:
#     if papers_annotated[paper_id]["status"] == "done":
#         print(paper_id)
#         print(papers_annotated[paper_id])
#         pdf_file = os.path.join(pdf_folder, paper_id + ".pdf")
#         filepath = pathlib.Path(pdf_file)
#         prompt = open("prompt_annotating.txt").read().strip()
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=[
#                 types.Part.from_bytes(
#                     data=filepath.read_bytes(),
#                     mime_type='application/pdf',
#                     ),
#                 prompt])
#         print(response.text)
#         try:
#             if response.text.startswith("{"):
#                 output_json = json.loads(response.text)
#             elif response.text.startswith("```json"):
#                 output_json = json.loads(response.text[7:-3].strip())
#             else:
#                 output_json = json.loads(response.text)
#             print(output_json)
#             if output_json["reference_count"] == papers_annotated[paper_id]["referenceCount"]:
#                 results_references.append(1)
#             else:
#                 results_references.append(0)
#             if output_json["authors"] == papers_annotated[paper_id]["authors"]:
#                 results_authors.append(1)
#             else:
#                 results_authors.append(0)
#             if output_json["title"] == papers_annotated[paper_id]["title"]:
#                 results_titles.append(1)
#             else:
#                 results_titles.append(0)
#         except Exception as e:
#             print(e)
#         time.sleep(10)
# print("results", sum(results_references), sum(results_authors), sum(results_titles), len(results_titles))
# # results 37 37 33 38

# annotate all samples not done by humans
with open("papers_gemini.json") as f:
    papers_gemini = json.load(f)

pdf_folder = "../pdfs"
paper_ids = list(papers_gemini.keys())
random.shuffle(paper_ids)

for paper_id in paper_ids:
    if papers_gemini[paper_id]["status"] != "done":
        print(paper_id)
        print(papers_gemini[paper_id])
        pdf_file = os.path.join(pdf_folder, paper_id + ".pdf")
        filepath = pathlib.Path(pdf_file)
        prompt = open("prompt_annotating.txt").read().strip()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=filepath.read_bytes(),
                    mime_type='application/pdf',
                    ),
                prompt])
        print(response.text)
        try:
            if response.text.startswith("{"):
                output_json = json.loads(response.text)
            elif response.text.startswith("```json"):
                output_json = json.loads(response.text[7:-3].strip())
            else:
                output_json = json.loads(response.text)
            print(output_json)

            output_json_keys = list(output_json.keys())
            if "authors" in output_json_keys and "title" in output_json_keys and "reference_count" in output_json_keys:
                papers_gemini[paper_id]["authors"] = output_json["authors"]
                papers_gemini[paper_id]["title"] = output_json["title"]
                papers_gemini[paper_id]["referenceCount"] = output_json["reference_count"]
                papers_gemini[paper_id]["status"] = "done"
                with open("papers_gemini.json", "w") as f:
                    json.dump(papers_gemini, f, indent=4)
        except Exception as e:
            print(e)
        time.sleep(10)


# calculate again the accuracy on reference count
with open("papers_gemini.json") as f:
    papers_gemini = json.load(f)
with open("papers_annotated.json") as f:
    papers_annotated = json.load(f)
results = []
for paper_id_annotated, paper_info_annotated in papers_annotated.items():
    if paper_info_annotated["status"] == "done reference" or paper_info_annotated["status"] == "done":
        paper_info_gemini = papers_gemini[paper_id_annotated]
        if paper_info_gemini["referenceCount"] == paper_info_annotated["referenceCount"]:
            results.append(1)
        else:
            results.append(0)
print("results", sum(results), len(results))
# results 132 141





