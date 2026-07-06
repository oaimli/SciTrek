import json
import os
import random
from tqdm import tqdm
from fuzzysearch import find_near_matches


# #  verify where the papers have pdfs
# with open("graphs.json") as f:
#     graphs = json.load(f)
#
# all_papers = {}
# for subtopic, graph in graphs.items():
#     # print(subtopic)
#     papers_detailed = {}
#     for paper_id, paper_details in graph.items():
#         if os.path.exists(f"../pdfs/{paper_id}.pdf"):
#             papers_detailed[paper_id] = paper_details
#             # copyfile(f"../pdfs/tmp/{paper_id}.pdf", f"../pdfs/{subtopic}/{paper_id}.pdf")
#     all_papers.update(papers_detailed)
#
#     print(subtopic, len(papers_detailed))
# print("all papers with pdfs:", len(all_papers))
#
#
# # verify the number of references
# invalid_papers = {}
# reference_info = []
# for paper_id, details in all_papers.items():
#     reference_count = details["referenceCount"]
#     references = details["references"]
#     references_title = details["references_title"]
#     if not (reference_count == len(references) == len(references_title)):
#         invalid_papers[paper_id] = details
#         # print(paper_id, reference_count, len(references), len(references_title))
#         reference_info.append([paper_id, reference_count, len(references), len(references_title)])
#
#     if reference_count < len(references):
#         print(paper_id, reference_count, len(references), len(references_title))
#         reference_info.append([paper_id, reference_count, len(references), len(references_title)])
#
# print("invalid papers:", len(invalid_papers))


# # verify the set of references and citations with text matching
# with open("papers.json") as f:
#     papers = json.load(f)
#
# # remove the references_title as every paper has it
# for paper_id, paper_info in papers.items():
#     del papers[paper_id]["references_title"]
#
# # remove papers without the section of references
# zero_references = set([])
# more_references = set([])
# for paper_id, paper_info in papers.items():
#     markdown = paper_info["markdown"].lower()
#     references_matches = find_near_matches("references", markdown, max_l_dist=0)
#     preferences_matches = find_near_matches("preferences", markdown, max_l_dist=0)
#     coreferences_matches = find_near_matches("coreferences", markdown, max_l_dist=0)
#     dereferences_matches = find_near_matches("dereferences", markdown, max_l_dist=0)
#     georeferences_matches = find_near_matches("georeferences", markdown, max_l_dist=0)
#     misreferences_matches = find_near_matches("misreferences", markdown, max_l_dist=0)
#     other_matches = preferences_matches + coreferences_matches + dereferences_matches + georeferences_matches + misreferences_matches
#     references_matches_real = []
#     for references_match in references_matches:
#         print("references", markdown[references_match.start:references_match.end], )
#         references_match_start = references_match.start
#         flag = 1
#         for other_match in other_matches:
#             print("other", markdown[other_match.start: other_match.end])
#             other_match_start = other_match.start
#             if abs(other_match_start - references_match_start) < 5:
#                 flag = 0
#         if flag == 1:
#             references_matches_real.append(references_match)
#     print(len(references_matches), len(references_matches_real))
#
#     if len(references_matches_real) == 0:
#         print(paper_id, "no references")
#         zero_references.add(paper_id)
#
#     if len(references_matches_real) > 1:
#         print(paper_id, references_matches_real[0].start, references_matches_real[0].end)
#         more_references.add(paper_id)
#     # else:
#     #     print(paper_id, references_matches[0].start, references_matches[0].end)
# print("invalid papers:", len(zero_references))
# print("more references:", len(more_references))
#
# for paper_id, paper_info in papers.items():
#     citations = paper_info["citations"]
#     references = paper_info["references"]
#     # remove those paper ids that are not in our dataset
#     citations_new = []
#     for citation in citations:
#         if citation in list(papers.keys()):
#             citations_new.append(citation)
#     assert len(citations_new) == len(set(citations_new))
#     references_new = []
#     for reference in references:
#         if reference in list(papers.keys()):
#             references_new.append(reference)
#     assert len(references_new) == len(set(references_new))
#     papers[paper_id]["citations"] = citations_new
#     papers[paper_id]["references"] = references_new
#
#     # make it consistent between citations and references
#     for citation in citations_new:
#         if paper_id not in papers[citation]["references"]:
#             print("reference added", paper_id, citation)
#             references_tmp = papers[citation]["references"]
#             references_tmp.append(paper_id)
#             papers[citation]["references"] = references_tmp
#
#     for reference in references_new:
#         if paper_id not in papers[reference]["citations"]:
#             print("citation added", paper_id, reference)
#             citations_tmp = papers[reference]["citations"]
#             citations_tmp.append(paper_id)
#             papers[reference]["citations"] = citations_tmp
#
# # verify the consistency between citations and references
# for paper_id, paper_info in papers.items():
#     citations = paper_info["citations"]
#     references = paper_info["references"]
#     # print(paper_id, len(citations), len(references))
#     for citation in citations:
#         if paper_id not in papers[citation]["references"]:
#             print("reference error", paper_id, citation)
#     for reference in references:
#         if paper_id not in papers[reference]["citations"]:
#             print("citation error", paper_id, reference)
#
# all_pairs = []
# wrong_pairs = []
# # verify references with fuzzysearch
# for paper_id, paper_info in papers.items():
#     references = paper_info["references"]
#     markdown = paper_info["markdown"].lower()
#     for reference in references:
#         reference_title = papers[reference]["title"]
#         if len(reference_title.split()) > 10:
#             threshold = 5
#         elif 10 >= len(reference_title.split()) > 5:
#             threshold = 3
#         else:
#             threshold = 1
#         matches = find_near_matches(reference_title, markdown, max_l_dist=threshold)
#         if len(matches) == 0:
#             wrong_pairs.append([paper_id, reference])
#         all_pairs.append([paper_id, reference])
#
# print("wrong pairs ratio:", len(wrong_pairs)/len(all_pairs))
#
# # with open("papers_correct.json", "w") as f:
# #     json.dump(papers, f, indent=4)
#
# # any more papers than the existing references
# for paper_id, paper_info in papers.items():
#     papers[paper_id]["references_original"] = paper_info["references"]
#     papers[paper_id]["citations_original"] = paper_info["citations"]
#     papers[paper_id]["references"] = []
#     papers[paper_id]["citations"] = []
#     papers[paper_id]["references_title"] = []
#     markdown = paper_info["markdown"]
#     del papers[paper_id]["markdown"]
#     papers[paper_id]["markdown"] = markdown
#
# for paper_i_id, paper_i_info in papers.items():
#     paper_i_markdown = paper_i_info["markdown"].lower()
#     for paper_j_id, paper_j_info in papers.items():
#         if paper_i_id != paper_j_id:
#             paper_j_info["title"] = " ".join(paper_j_info["title"].split())
#             paper_j_title = paper_j_info["title"].lower().strip()
#             if paper_i_markdown.find(paper_j_title) >= 0:
#                 if paper_j_id not in paper_i_info["references"]:
#                     paper_i_references = paper_i_info["references"]
#                     paper_i_references.append(paper_j_id)
#                     papers[paper_i_id]["references"] = paper_i_references
#                     paper_i_references_title = paper_i_info["references_title"]
#                     paper_i_references_title.append(paper_j_info["title"])
#                     papers[paper_i_id]["references_title"] = paper_i_references_title
#                 if paper_i_id not in paper_j_info["citations"]:
#                     paper_j_citations = paper_j_info["citations"]
#                     paper_j_citations.append(paper_i_id)
#                     papers[paper_j_id]["citations"] = paper_j_citations
#             else:
#                 paper_j_title_words = paper_j_title.split()
#                 if len(paper_j_title_words) > 10:
#                     threshold = 5
#                 elif 10 >= len(paper_j_title_words) > 5:
#                     threshold = 3
#                 else:
#                     threshold = 1
#                 title_matches = find_near_matches(paper_j_title, paper_i_markdown, max_l_dist=threshold)
#                 if len(title_matches) > 0:
#                     print(len(title_matches), paper_i_id, paper_j_id, paper_j_title)
#                     print(paper_j_title)
#                     print(paper_i_markdown[title_matches[0].start:title_matches[0].end], title_matches[0].start, title_matches[0].end)
#                     if paper_j_id not in paper_i_info["references"]:
#                         paper_i_references = paper_i_info["references"]
#                         paper_i_references.append(paper_j_id)
#                         papers[paper_i_id]["references"] = paper_i_references
#                         paper_i_references_title = paper_i_info["references_title"]
#                         paper_i_references_title.append(paper_j_info["title"])
#                         papers[paper_i_id]["references_title"] = paper_i_references_title
#                     if paper_i_id not in paper_j_info["citations"]:
#                         paper_j_citations = paper_j_info["citations"]
#                         paper_j_citations.append(paper_i_id)
#                         papers[paper_j_id]["citations"] = paper_j_citations
#
# # verify the consistency between citations and references
# for paper_id, paper_info in papers.items():
#     citations = paper_info["citations"]
#     references = paper_info["references"]
#     print(paper_id, len(citations), len(references))
#     for citation in citations:
#         if paper_id not in papers[citation]["references"]:
#             print(paper_id, citation)
#     for reference in references:
#         if paper_id not in papers[reference]["citations"]:
#             print(paper_id, reference)

with open("papers_correct.json") as f:
    papers_correct = json.load(f)

# removing papers that are too short or long
papers_remain = {}
no_abstract = 0
for paper_id, paper_info in papers_correct.items():
    if paper_info["abstract"] == None:
        print("No abstract in paper", paper_id)
        no_abstract += 1
    else:
        if len(paper_info["abstract"]) == 0:
            print("Abstract empty in paper", paper_id)
            no_abstract += 1

    length = paper_info["length"]
    if 5000 < length < 50000:
        papers_remain[paper_id] = paper_info
print(len(papers_remain), no_abstract)

# with open("papers_correct.json", "w") as f:
#     json.dump(papers_remain, f, indent=4)



