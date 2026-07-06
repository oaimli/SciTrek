import json
import os


if __name__ == "__main__":
    markdown_folder = "../md_gemini/"

    markdown_filenames = []
    for markdown_filename in os.listdir(markdown_folder):
        if markdown_filename.endswith(".md"):
            markdown_filenames.append(markdown_filename)

    for markdown_filename in markdown_filenames:
        if open(os.path.join(markdown_folder, markdown_filename)).read().strip() == "":
            print(markdown_filename)

    with open("papers_final.json") as f:
        papers_final = json.load(f)
    paper_id = "41aaf65390f117311c650a1971e99083d5eaf027"
    md_file = os.path.join(markdown_folder, paper_id + ".md")
    papers_final[paper_id]["markdown"] = open(md_file).read().strip()
    print(papers_final[paper_id]["markdown"])

    with open("papers_final0.json", "w") as f:
        json.dump(papers_final, f, indent=4)




