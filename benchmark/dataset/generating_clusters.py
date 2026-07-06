import json
import random
from typing import Dict

import jsonlines

from citation_graph import PapersGraph
from tqdm import tqdm


# get the set of papers randomly
def get_batch_random(paper_id_start: str, papers: Dict, max_length: int, smallest_count):
    batch = []
    batch_tmp = []
    lengths_tmp = []
    batch_tmp.append(paper_id_start)
    lengths_tmp.append(papers[paper_id_start]["length"])

    all_paper_ids = list(papers.keys())
    other_paper_ids = []
    for paper_id in all_paper_ids:
        if paper_id != paper_id_start:
            other_paper_ids.append(paper_id)

    random.shuffle(other_paper_ids)
    for i, paper_id in enumerate(other_paper_ids):
        batch_tmp.append(paper_id)
        lengths_tmp.append(papers[paper_id]["length"])
        paper_id_next = other_paper_ids[i + 1] if i + 1 < len(other_paper_ids) else other_paper_ids[0]
        length_next = papers[paper_id_next]["length"]
        if len(batch_tmp) >= smallest_count and sum(lengths_tmp) + length_next > max_length and sum(
                lengths_tmp) <= max_length:
            batch = batch_tmp
            break
    random.shuffle(batch)
    return batch


# get the set of papers based on the citation graph
def get_batch_graph(paper_id_start: str, papers: Dict, max_length: int, smallest_count: int):
    all_paper_ids = list(papers.keys())
    papers_list = []
    paper_start = {}
    for paper_id, paper_details in papers.items():
        references_raw = paper_details["references"]
        citations_raw = paper_details["citations"]
        references_filtered = []
        for reference in references_raw:
            if reference in all_paper_ids:
                references_filtered.append(reference)
        citations_filtered = []
        for citation in citations_raw:
            if citation in all_paper_ids:
                citations_filtered.append(citation)
        paper = {"paper_id": paper_id, "length": paper_details["length"], "references": references_filtered,
                 "citations": citations_filtered}
        if paper_id == paper_id_start:
            paper_start = paper
        papers_list.append(paper)
    assert paper_id_start in list(papers.keys())

    papers_graph = PapersGraph(papers_list)

    dfs_result = papers_graph.dfs_traverse(paper_start, max_length)
    batch_dfs = []
    batch_dfs_tmp = []
    batch_dfs_lengths_tmp = []
    for i, tmp_paper_id in enumerate(dfs_result):
        batch_dfs_lengths_tmp.append(papers[tmp_paper_id]["length"])
        batch_dfs_tmp.append(tmp_paper_id)

        paper_id_next = dfs_result[i + 1] if i + 1 < len(dfs_result) else dfs_result[0]
        paper_next = papers[paper_id_next]
        paper_next_length = paper_next["length"]
        if len(batch_dfs_tmp) >= smallest_count and sum(batch_dfs_lengths_tmp) + paper_next_length > max_length and sum(
                batch_dfs_lengths_tmp) <= max_length:
            batch_dfs = batch_dfs_tmp
            # print(sum(batch_dfs_lengths_tmp), max_length, len(dfs_result), len(batch_dfs))
            break

    bfs_result = papers_graph.bfs_traverse(paper_start, max_length)
    batch_bfs = []
    batch_bfs_tmp = []
    batch_bfs_lengths_tmp = []
    for i, tmp_paper_id in enumerate(bfs_result):
        batch_bfs_lengths_tmp.append(papers[tmp_paper_id]["length"])
        batch_bfs_tmp.append(tmp_paper_id)

        paper_id_next = bfs_result[i + 1] if i + 1 < len(bfs_result) else bfs_result[0]
        paper_next = papers[paper_id_next]
        paper_next_length = paper_next["length"]
        if len(batch_bfs_tmp) >= smallest_count and sum(batch_bfs_lengths_tmp) + paper_next_length > max_length and sum(
                batch_bfs_lengths_tmp) <= max_length:
            batch_bfs = batch_bfs_tmp
            # print(sum(batch_bfs_lengths_tmp), max_length, len(bfs_result), len(batch_bfs))
            break
    # print(len(batch_bfs), len(batch_dfs))
    random.shuffle(batch_bfs)
    random.shuffle(batch_dfs)
    return [batch_bfs, batch_dfs]


if __name__ == "__main__":

    # random.seed(42)
    with open("../article/papers_correct.json") as f:
        papers = json.load(f)
    paper_ids = list(papers.keys())
    random.shuffle(paper_ids)

    test = []
    for paper_id, paper_info in tqdm(papers.items()):
        test.append({"papers": [paper_id], "level": "single"})
    with jsonlines.open("clusters/single_clusters_all.jsonl", "w") as writer:
        writer.write_all(test)
    print("single_all", len(test))

    for level in [64, 128, 512, 1024]:
        max_length = level * 1024
        print("max_length", max_length)
        smallest_count = 4

        test = []
        test_candidates_random = []
        for paper_id in tqdm(paper_ids):
            batch = get_batch_random(paper_id, papers, max_length, smallest_count)
            if len(batch) >= smallest_count:
                overlapping = 0
                for test_words_candidate_random in test_candidates_random:
                    intersection = set(batch).intersection(set(test_words_candidate_random["papers"]))
                    if len(intersection) / len(batch) >= 0.5 or len(intersection) / len(
                            test_words_candidate_random["papers"]) >= 0.5:
                        overlapping = 1
                if overlapping == 0:
                    entire = {"papers": batch, "level": f"multi_ran_{level}"}
                    test_candidates_random.append(entire)
        test.extend(test_candidates_random)
        print("test_candidates_random", len(test_candidates_random))

        test_candidates_graph = []
        for paper_id in tqdm(paper_ids):
            batches = get_batch_graph(paper_id, papers, max_length, smallest_count)
            assert len(batches) == 2
            if len(batches[0]) >= smallest_count:
                overlapping = 0
                for test_words_candidate_graph in test_candidates_graph:
                    intersection = set(batches[0]).intersection(set(test_words_candidate_graph["papers"]))
                    if len(intersection) / len(batches[0]) >= 0.5 or len(intersection) / len(
                            test_words_candidate_graph["papers"]) >= 0.5:
                        overlapping = 1
                if overlapping == 0:
                    entire_0 = {"papers": batches[0], "level": f"multi_bfs_{level}"}
                    test_candidates_graph.append(entire_0)

            if len(batches[1]) >= smallest_count:
                overlapping = 0
                for test_words_candidate_graph in test_candidates_graph:
                    intersection = set(batches[1]).intersection(set(test_words_candidate_graph["papers"]))
                    if len(intersection) / len(batches[1]) >= 0.5 or len(intersection) / len(
                            test_words_candidate_graph["papers"]) >= 0.5:
                        overlapping = 1
                if overlapping == 0:
                    entire_1 = {"papers": batches[1], "level": f"multi_dfs_{level}"}
                    test_candidates_graph.append(entire_1)
        test.extend(test_candidates_graph)
        print("test_candidates_graph", len(test_candidates_graph))

        if max_length == 64 * 1024:
            print("all_64k", len(test))
            with jsonlines.open("clusters/64k_clusters_all.jsonl", "w") as writer:
                writer.write_all(test)
        if max_length == 128 * 1024:
            print("all_128k", len(test))
            with jsonlines.open("clusters/128k_clusters_all.jsonl", "w") as writer:
                writer.write_all(test)
        if max_length == 512 * 1024:
            print("all_512k", len(test))
            with jsonlines.open("clusters/512k_clusters_all.jsonl", "w") as writer:
                writer.write_all(test)
        if max_length == 1024 * 1024:
            print("all_1024k", len(test))
            with jsonlines.open("clusters/1024k_clusters_all.jsonl", "w") as writer:
                writer.write_all(test)
