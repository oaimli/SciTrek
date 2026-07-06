import random
import numpy as np
from typing import List

class PapersGraph():
    '''
    each paper has the following key attributes:
    - paper_id
    - references
    - citations
    '''
    def __init__(self, papers: List):
        self.papers = papers
        self.papers_dict = {}
        self.paper_ids = []
        for paper in papers:
            self.papers_dict[paper["paper_id"]] = paper
            self.paper_ids.append(paper["paper_id"])


    def dfs_traverse(self, paper, max_length):
        related_paper_ids = []
        related_paper_lengths = []
        while sum(related_paper_lengths) < max_length:
            if len(related_paper_ids) == 0:
                free_paper = paper
            else:
                free_paper_ids = []
                for paper_id in self.paper_ids:
                    if paper_id not in related_paper_ids:
                        free_paper_ids.append(paper_id)
                free_paper = self.papers_dict[random.sample(free_paper_ids, 1)[0]]
            # depth first, stack
            tmp_paper_ids = []
            tmp_paper_ids_all = [] # record all arrived paper
            tmp_paper_ids.append(free_paper["paper_id"])
            tmp_paper_ids_all.append(free_paper["paper_id"])
            while len(tmp_paper_ids) > 0:
                tmp_paper_id = tmp_paper_ids.pop()
                if sum(related_paper_lengths) < max_length:
                    related_paper_ids.append(tmp_paper_id)
                    related_paper_lengths.append(self.papers_dict[tmp_paper_id]["length"])
                else:
                    break
                # print("related_paper_ids", len(related_paper_ids))
                paper_tmp = self.papers_dict[tmp_paper_id]
                connected_paper_ids = paper_tmp["references"] + paper_tmp["citations"]
                random.shuffle(connected_paper_ids)
                for connected_paper_id in connected_paper_ids:
                    if connected_paper_id not in tmp_paper_ids_all:
                        tmp_paper_ids.append(connected_paper_id)
                        tmp_paper_ids_all.append(connected_paper_id)

        return related_paper_ids

    def bfs_traverse(self, paper, max_length):
        # breadth first, queue
        related_paper_ids = []
        related_paper_lengths = []
        while sum(related_paper_lengths) < max_length :
            if len(related_paper_ids) == 0:
                free_paper = paper
            else:
                free_paper_ids = []
                for paper_id in self.paper_ids:
                    if paper_id not in related_paper_ids:
                        free_paper_ids.append(paper_id)
                free_paper = self.papers_dict[random.sample(free_paper_ids, 1)[0]]
            tmp_paper_ids = []
            tmp_paper_ids_all = []  # record all arrived paper
            tmp_paper_ids.append(free_paper["paper_id"])
            tmp_paper_ids_all.append(free_paper["paper_id"])
            while len(tmp_paper_ids) > 0:
                tmp_paper_id = tmp_paper_ids.pop(0)
                if sum(related_paper_lengths) < max_length:
                    related_paper_ids.append(tmp_paper_id)
                    related_paper_lengths.append(self.papers_dict[tmp_paper_id]["length"])
                else:
                    break
                paper_tmp = self.papers_dict[tmp_paper_id]
                connected_paper_ids = paper_tmp["references"] + paper_tmp["citations"]
                random.shuffle(connected_paper_ids)
                for connected_paper_id in connected_paper_ids:
                    if connected_paper_id not in tmp_paper_ids_all:
                        tmp_paper_ids.append(connected_paper_id)
                        tmp_paper_ids_all.append(connected_paper_id)

        return related_paper_ids

    def shortest_path(self, paper_pre, paper_suffix):
        path = []
        return path


if __name__ == "__main__":
    # test graph algorithms to get related papers
    #     8 0
    #     |/|\
    #     1 2 3
    #    /|\|/
    #   4 5 6
    #       |
    #       7
    #
    #       a
    #      /|\
    #     b c d
    #     |
    #     e
    #
    #       f
    papers = []
    paper_0 = {"paper_id": "0", "references": ["1", "2", "3"], "citations": [], "length": 1}
    papers.append(paper_0)
    paper_1 = {"paper_id": "1", "references": ["4", "5", "6"], "citations": ["0", "8"], "length": 1}
    papers.append(paper_1)
    paper_2 = {"paper_id": "2", "references": ["6"], "citations": ["0"], "length": 1}
    papers.append(paper_2)
    paper_3 = {"paper_id": "3", "references": ["6"], "citations": ["0"], "length": 1}
    papers.append(paper_3)
    paper_4 = {"paper_id": "4", "references": [], "citations": ["1"], "length": 1}
    papers.append(paper_4)
    paper_5 = {"paper_id": "5", "references": [], "citations": ["1"], "length": 1}
    papers.append(paper_5)
    paper_6 = {"paper_id": "6", "references": ["7"], "citations": ["1", "2", "3"], "length": 1}
    papers.append(paper_6)
    paper_7 = {"paper_id": "7", "references": [], "citations": ["6"], "length": 1}
    papers.append(paper_7)
    paper_8 = {"paper_id": "8", "references": ["1"], "citations": [], "length": 1}
    papers.append(paper_8)
    paper_a = {"paper_id": "a", "references": ["b", "c", "d"], "citations": [], "length": 1}
    papers.append(paper_a)
    paper_b = {"paper_id": "b", "references": ["e"], "citations": ["a"], "length": 1}
    papers.append(paper_b)
    paper_c = {"paper_id": "c", "references": [], "citations": ["a"], "length": 1}
    papers.append(paper_c)
    paper_d = {"paper_id": "d", "references": [], "citations": ["a"], "length": 1}
    papers.append(paper_d)
    paper_e = {"paper_id": "e", "references": [], "citations": ["b"], "length": 1}
    papers.append(paper_e)
    paper_f = {"paper_id": "f", "references": [], "citations": [], "length": 1}
    papers.append(paper_f)

    papers_graph = PapersGraph(papers)
    print("dfs_traverse")
    print(papers_graph.dfs_traverse(paper_0, len(papers)))
    print(papers_graph.dfs_traverse(paper_1, len(papers)))
    print(papers_graph.dfs_traverse(paper_2, len(papers)))
    print(papers_graph.dfs_traverse(paper_3, len(papers)))
    print(papers_graph.dfs_traverse(paper_4, len(papers)))
    print(papers_graph.dfs_traverse(paper_5, len(papers)))
    print(papers_graph.dfs_traverse(paper_6, len(papers)))
    print(papers_graph.dfs_traverse(paper_7, len(papers)))
    print(papers_graph.dfs_traverse(paper_8, len(papers)))
    print(papers_graph.dfs_traverse(paper_a, len(papers)))
    print(papers_graph.dfs_traverse(paper_b, len(papers)))
    print(papers_graph.dfs_traverse(paper_c, len(papers)))
    print(papers_graph.dfs_traverse(paper_d, len(papers)))
    print(papers_graph.dfs_traverse(paper_e, len(papers)))
    print(papers_graph.dfs_traverse(paper_f, len(papers)))
    print("bfs_traverse")
    print(papers_graph.bfs_traverse(paper_0, len(papers)))
    print(papers_graph.bfs_traverse(paper_1, len(papers)))
    print(papers_graph.bfs_traverse(paper_2, len(papers)))
    print(papers_graph.bfs_traverse(paper_3, len(papers)))
    print(papers_graph.bfs_traverse(paper_4, len(papers)))
    print(papers_graph.bfs_traverse(paper_5, len(papers)))
    print(papers_graph.bfs_traverse(paper_6, len(papers)))
    print(papers_graph.bfs_traverse(paper_7, len(papers)))
    print(papers_graph.bfs_traverse(paper_8, len(papers)))
    print(papers_graph.bfs_traverse(paper_a, len(papers)))
    print(papers_graph.bfs_traverse(paper_b, len(papers)))
    print(papers_graph.bfs_traverse(paper_c, len(papers)))
    print(papers_graph.bfs_traverse(paper_d, len(papers)))
    print(papers_graph.bfs_traverse(paper_e, len(papers)))
    print(papers_graph.bfs_traverse(paper_f, len(papers)))
