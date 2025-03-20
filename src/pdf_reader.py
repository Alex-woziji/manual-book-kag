import pymupdf4llm
import os
import json

root_path = "../data/pdf"
files = os.listdir(root_path)

for f in files:
    pdf_document = os.path.join(root_path,f)
    photo_folder = os.path.join("../photo", f)
    os.makedirs(photo_folder)
    md_text = pymupdf4llm.to_markdown(pdf_document, page_chunks=True, write_images=True,
                                      image_path=photo_folder,
                                      margins=(0, 30, 0, 0), extract_words=True)
    page_content = {}
    for id, page in enumerate(md_text):
        page_content[id] = page['text']
    file_path = f"ingested_content/{f}.json"
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(page_content, json_file, ensure_ascii=False, indent=4)
