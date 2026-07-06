# https://api.semanticscholar.org/api-docs/
import os
import time
import json
import random
import jsonlines
import requests

S2_API_KEY = os.getenv('uenAKy0WRk7rfyLTLd4pB859pLvmtewg7H00Y2ci')


def get_details(semantic_scholar_id, time_sleep=5):
    # rsp = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/{semantic_scholar_id}',
    #                    headers={'X-API-KEY': S2_API_KEY},
    #                    params={'fields': 'authors,abstract,url,title,year,citations,references.title,referenceCount'})
    details = {}
    while True:
        rsp = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/{semantic_scholar_id}',
                           params={'fields': 'authors,abstract,url,title,year,citations,references.title,referenceCount,openAccessPdf'})
        if rsp.status_code == 200:
            citations = []
            for citation in rsp.json()['citations']:
                citation_id = citation['paperId']
                if citation_id != None:
                    citations.append(citation_id)
            references = []
            references_title = []
            for reference in rsp.json()['references']:
                reference_id = reference['paperId']
                if reference_id != None:
                    references_title.append(reference['title'])
                    references.append(reference_id)

            details["title"] = rsp.json()['title']
            details["year"] = rsp.json()['year']
            details["url"] = rsp.json()['url']
            details["authors"] = rsp.json()['authors']
            details["abstract"] = rsp.json()['abstract']
            details["referenceCount"] = rsp.json()['referenceCount']
            details["citations"] = citations
            details["references"] = references
            details["references_title"] = references_title
            details["pdf_access"] = rsp.json()['openAccessPdf']
            break
        else:
            print("response error", rsp.status_code)
            time.sleep(time_sleep)

    return details


def get_graph(semantic_scholar_id, graph_file, all_papers, max_first=10, max_second=5):
    if semantic_scholar_id in all_papers.keys():
        details_first = all_papers[semantic_scholar_id]
        print(semantic_scholar_id, "loaded")
    else:
        details_first = get_details(semantic_scholar_id)
        all_papers[semantic_scholar_id] = details_first
        with open(graph_file, "w") as f:
            json.dump(all_papers, f, indent=4)
        print(semantic_scholar_id, "downloaded")

    citations_first = details_first['citations']
    references_first = details_first['references']
    if len(citations_first) > max_first:
        citations_first_sampled = random.sample(citations_first, max_first)
    else:
        citations_first_sampled = citations_first
    if len(references_first) > max_first:
        references_first_sampled = random.sample(references_first, max_first)
    else:
        references_first_sampled = references_first
    related_papers = citations_first_sampled + references_first_sampled
    for related_paper in related_papers:
        if related_paper in all_papers.keys():
            details_second = all_papers[related_paper]
            print(related_paper, "loaded")
        else:
            details_second = get_details(related_paper)
            all_papers[related_paper] = details_second
            with open(graph_file, "w") as f:
                json.dump(all_papers, f, indent=4)
            print(related_paper, "downloaded")

        citations_second = details_second['citations']
        references_second = details_second['references']
        if len(citations_second) > max_second:
            citations_second_sampled = random.sample(citations_second, max_second)
        else:
            citations_second_sampled = citations_second
        if len(references_second) > max_second:
            references_second_sampled = random.sample(references_second, max_second)
        else:
            references_second_sampled = references_second
        other_papers = citations_second_sampled + references_second_sampled
        for other_paper in other_papers:
            if other_paper not in all_papers.keys():
                details_third = get_details(other_paper)
                all_papers[other_paper] = details_third
                with open(graph_file, "w") as f:
                    json.dump(all_papers, f, indent=4)
                print(other_paper, "downloaded")
            else:
                print(other_paper, "loaded")

    print("all_papers:", len(all_papers))

    return all_papers


if __name__ == '__main__':
    random.seed(42)
    starting_papers = []
    with jsonlines.open("meta.jsonl") as reader:
        for line in reader:
            starting_papers.append(line)

    for starting_paper in starting_papers:
        print(starting_paper)
        topic = starting_paper["topic"]
        graph_file = f"graphs/{topic}.json"

        if os.path.exists(graph_file):
            with open(graph_file) as f:
                all_papers = json.load(f)
        else:
            all_papers = {}
        print("existing papers:", len(all_papers))

        get_graph(starting_paper["semantic_scholar_id"], graph_file, all_papers)