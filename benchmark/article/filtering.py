# filtering out some papers from the citation graphs
import json
import os

graphs = {}
all_count = 0
for graph_file in os.listdir("graphs"):
    if graph_file.endswith(".json"):
        print(graph_file)
        graph_path = os.path.join("graphs", graph_file)
        with open(graph_path, "r") as f:
            graph = json.load(f)

        print("original papers", len(graph))

        all_paper_ids = list(graph.keys())
        new_papers = {}
        for key, value in graph.items():
            related = set(value["citations"] + value["references"])
            intersection = set(all_paper_ids).intersection(related)
            if len(intersection) > 4 and len(value["citations"]) > 0 and len(value["references"]) > 0:
                new_papers[key] = value

        print("new papers", len(new_papers))

        with open(os.path.join("filtered", graph_file), "w") as f:
            json.dump(new_papers, f, indent=4)

        graphs[graph_file.split(".")[0]] = new_papers
        all_count += len(new_papers)

print("all papers", all_count)
with open("graphs.json", "w") as f:
    json.dump(graphs, f, indent=4)