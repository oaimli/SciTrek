# get the source articles

# get papers with ids and details from semantic scholar with graphing.py based on meta.jsonl, into the folder of graphs
# filtering out some papers with few connections into the folder of filtered, and save the graphs into graphs.json
# download pdfs for all papers in graphs.json with scripts in the folder of pdfing, into the folder of pdfs
# analyze the pdf completeness in the folder of pdfs with analyzing.py
# transform pdfs into markdown with markdown.py, into the folder of markdown
# combine all markdown documents in markdown and graphs.json into a single file of article list in papers.json with combining.py
# analyzing the quality of markdown and the paper details from semantic scholar with analyzing.py
# verify the metadata and correcting references and citations with verifying.py, obtain papers_correct.json
# manually update some metadata including titles, authors and reference counts based on human annotation, annotating.py, get papers_annotated.json
# combine all the updated data including papers_gemini.json and Markdown by Gemini into papers_final.json, finalizing.py

# some citation or reference articles are not included in target articles in papers_final.json or papers_correct.json, as the length-based filtering in verifying.py