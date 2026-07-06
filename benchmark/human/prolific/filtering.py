import os
import jsonlines
import json

if __name__ == "__main__":
    # valid instances
    annotation_folder = "2025071802"
    instance_annotation_numbers = {}
    with jsonlines.open(f"annotations/{annotation_folder}/annotated_instances.jsonl") as reader:
        for line in reader:
            if line["meta"]["sql_type"] != "multi_simple":
                instance_annotation_numbers[line["instance_id"]] = instance_annotation_numbers.get(line["instance_id"], 0) + 1
    print("all instances:", len(list(instance_annotation_numbers.keys())))
    valid_instances = set([])
    for instance_id, instance_annotation_number in instance_annotation_numbers.items():
        if instance_annotation_number != 3:
            print("invalid", instance_id, instance_annotation_number)
        else:
            valid_instances.add(instance_id)
    print("valid instances:", len(list(valid_instances)))

    # group the annotations
    valid_annotations = {}
    with jsonlines.open(f"annotations/{annotation_folder}/annotated_instances.jsonl") as reader:
        for line in reader:
            if not line["instance_id"].endswith("_testing") and line["meta"]["sql_type"] != "multi_simple" and line["instance_id"] in valid_instances:
                tmp = valid_annotations.get(line["instance_id"], {})
                tmp["sql_type"] = line["meta"]["sql_type"]
                tmp["question"] = line["meta"]["question"]
                tmp["answer"] = line["meta"]["answer"]

                annotation = line["label_annotations"]["answer"]["text_box"]
                annotation = " ".join(annotation.split())
                annotation = ", ".join([anno.strip() for anno in annotation.split(",")])

                annotator_answers = tmp.get("annotations", {})
                annotator_answers[line["user_id"]] = annotation
                tmp["annotations"] = annotator_answers
                valid_annotations[line["instance_id"]] = tmp
    print("valid annotations:", len(valid_annotations))

    # agreement and alignment based on exact match
    for instance_id, details in valid_annotations.items():
        annotator_answers = list(details["annotations"].values())
        answer = details["answer"]

        aligned = []
        for annotator_answer in annotator_answers:
            if annotator_answer == answer:
                aligned.append(1)
            else:
                aligned.append(0)
        valid_annotations[instance_id]["aligned"] = sum(aligned)

        agreed = []
        for i, annotator_answer_i in enumerate(annotator_answers):
            for j, annotator_answer_j in enumerate(annotator_answers):
                if j > i:
                    if annotator_answer_i == annotator_answer_j:
                        agreed.append(1)
                    else:
                        agreed.append(0)
        if sum(agreed) >= 1:
            valid_annotations[instance_id]["agreed"] = 1
        else:
            valid_annotations[instance_id]["agreed"] = 0


    with open("analysis/quality_check_em.json", "w") as f:
        json.dump(valid_annotations, f, indent=4)

