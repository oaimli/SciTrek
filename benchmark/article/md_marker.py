import json
import os
from tqdm import tqdm
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser
from PIL import Image

config = {
    "output_format": "markdown",
    "use_llm": "",
    "openai_api_key": "",
    "openai_model": "gpt-4o-2024-11-20",
    "openai_base_url": "https://api.openai.com",
    "llm_service": "marker.services.openai.OpenAIService"
}
config_parser = ConfigParser(config)
converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
    llm_service=config_parser.get_llm_service()
)

with open("graphs.json") as f:
    graphs = json.load(f)

# not all pdfs are used in the folder of pdfs
all_papers_id = []
for subtopic, graph in graphs.items():
    for paper_id, paper_details in graph.items():
        if os.path.exists(f"../pdfs/{paper_id}.pdf"):
            all_papers_id.append(paper_id)
print("all valid papers:", len(all_papers_id))

for paper_id in tqdm(all_papers_id):
    pdf_path = f"../pdfs/{paper_id}.pdf"
    md_path = f"../markdown/{paper_id}"
    os.makedirs(md_path, exist_ok=True)
    text_path = os.path.join(md_path, f"{paper_id}.md")

    if not os.path.exists(text_path):
        print(paper_id)
        rendered = converter(pdf_path)
        text, _, images = text_from_rendered(rendered)

        with open(text_path, "w") as f:
            f.write(text)
        # print(images.keys())
        for key, value in images.items():
            if isinstance(value, Image.Image):
                value.save(os.path.join(md_path, key))
    else:
        print("markdown exists:", paper_id)


