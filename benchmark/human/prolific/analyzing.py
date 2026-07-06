import os

import jsonlines
import json

if __name__ == "__main__":
    with open("analysis/quality_check_nor.json") as f:
        quality_check = json.load(f)
    agreed_results = []
    aligned_results = []
    category_results = {}
    for instance_id, details in quality_check.items():
        assert len(list(details.keys())) == 6
        # if details["answer"] != "NULL":
        agreed_results.append(details["agreed"])
        if details["aligned"] >= 2:
            aligned_results.append(1)
        else:
            aligned_results.append(0)
        tmp = category_results.get(details["sql_type"], [])
        tmp.append((details["aligned"], details["agreed"]))
        category_results[details["sql_type"]] = tmp
    print("Agreement", sum(agreed_results), len(agreed_results) * 1, sum(agreed_results) / (len(agreed_results) * 1))
    print("Alignment", sum(aligned_results), len(aligned_results) * 1, sum(aligned_results) / (len(aligned_results) * 1))


    print("Results in different SQL types")
    for category, alignment_agreement in category_results.items():
        print(category)
        aligned = []
        agreed = []
        for tmp in alignment_agreement:
            if tmp[0] >= 2:
                aligned.append(1)
            else:
                aligned.append(0)
            agreed.append(tmp[1])
        print("agreement", sum(agreed), len(agreed) * 1, sum(agreed) / (len(agreed) * 1))
        print("alignment", sum(aligned), len(aligned) * 1, sum(aligned) / (len(aligned) * 1))
