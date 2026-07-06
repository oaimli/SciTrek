import jsonlines
import numpy as np
import json


with open("../construction/papers_correct.json") as f:
    papers = json.load(f)

test_single = []
with jsonlines.open("clusters/single_clusters_all.jsonl") as reader:
    for line in reader:
        test_single.append(line)
papers_counts = []
cluster_lengths = []
for instance in test_single:
    papers_counts.append(len(instance["papers"]))
    cluster_length = []
    for paper_id in instance["papers"]:
        cluster_length.append(papers[paper_id]["length"])
    cluster_lengths.append(np.sum(cluster_length))
print("single_all", len(test_single))
print("average count of papers, single", np.mean(papers_counts), min(papers_counts), max(papers_counts))
print("average length of clusters, single", np.mean(cluster_lengths), min(cluster_lengths), max(cluster_lengths))

papers_ids = set([])

test_64k = []
with jsonlines.open("clusters/64k_clusters_all.jsonl") as reader:
    for line in reader:
        test_64k.append(line)
papers_counts = []
cluster_lengths = []
for instance in test_64k:
    papers_counts.append(len(instance["papers"]))
    papers_ids.update(instance["papers"])
    cluster_length = []
    for paper_id in instance["papers"]:
        cluster_length.append(papers[paper_id]["length"])
    cluster_lengths.append(np.sum(cluster_length))
print("64k_all", len(test_64k))
print("average count of papers, 64k", np.mean(papers_counts), min(papers_counts), max(papers_counts))
print("average length of clusters, 64k", np.mean(cluster_lengths), min(cluster_lengths), max(cluster_lengths))


test_128k = []
with jsonlines.open("clusters/128k_clusters_all.jsonl") as reader:
    for line in reader:
        test_128k.append(line)
papers_counts = []
cluster_lengths = []
for instance in test_128k:
    papers_counts.append(len(instance["papers"]))
    papers_ids.update(instance["papers"])
    cluster_length = []
    for paper_id in instance["papers"]:
        cluster_length.append(papers[paper_id]["length"])
    cluster_lengths.append(np.sum(cluster_length))
print("128k_all", len(test_128k))
print("average count of papers, 128k", np.mean(papers_counts), min(papers_counts), max(papers_counts))
print("average length of clusters, 128k", np.mean(cluster_lengths), min(cluster_lengths), max(cluster_lengths))

test_512k = []
with jsonlines.open("clusters/512k_clusters_all.jsonl") as reader:
    for line in reader:
        test_512k.append(line)
papers_counts = []
cluster_lengths = []
for instance in test_512k:
    papers_counts.append(len(instance["papers"]))
    papers_ids.update(instance["papers"])
    cluster_length = []
    for paper_id in instance["papers"]:
        cluster_length.append(papers[paper_id]["length"])
    cluster_lengths.append(np.sum(cluster_length))
print("512k_all", len(test_512k))
print("average count of papers, 512k", np.mean(papers_counts), min(papers_counts), max(papers_counts))
print("average length of clusters, 512k", np.mean(cluster_lengths), min(cluster_lengths), max(cluster_lengths))

test_1024k = []
with jsonlines.open("clusters/1024k_clusters_all.jsonl") as reader:
    for line in reader:
        test_1024k.append(line)
papers_counts = []
cluster_lengths = []
for instance in test_1024k:
    papers_counts.append(len(instance["papers"]))
    papers_ids.update(instance["papers"])
    cluster_length = []
    for paper_id in instance["papers"]:
        cluster_length.append(papers[paper_id]["length"])
    cluster_lengths.append(np.sum(cluster_length))
print("1024k_all", len(test_1024k))
print("average count of papers, 1024k", np.mean(papers_counts), min(papers_counts), max(papers_counts))
print("average length of clusters, 1024k", np.mean(cluster_lengths), min(cluster_lengths), max(cluster_lengths))

print("paper coverage", len(papers_ids))