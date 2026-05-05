import fitz
import os
from base_extractor import BaseExtractor

class PyMuPDFExtractor(BaseExtractor):
    def __init__(self, pdf_path: str, image_dir="images"):
        self.pdf_path = pdf_path
        self.image_dir = image_dir
        os.makedirs(image_dir, exist_ok=True)

    def extract(self):
        doc = fitz.open(self.pdf_path)
        elements = []

        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if block["type"] == 0:
                    text = " ".join(
                        span["text"]
                        for line in block.get("lines", [])
                        for span in line.get("spans", [])
                    ).strip()

                    if text:
                        elements.append({
                            "type": "text",
                            "content": text,
                            "page": page_num,
                            "bbox": block["bbox"],
                            "metadata": {"source": "pymupdf"}
                        })

                elif block["type"] == 1:
                    xref = block["image"]
                    img = doc.extract_image(xref)

                    path = os.path.join(
                        self.image_dir,
                        f"page{page_num}_{xref}.png"
                    )

                    with open(path, "wb") as f:
                        f.write(img["image"])

                    elements.append({
                        "type": "image",
                        "content": path,
                        "page": page_num,
                        "bbox": block["bbox"],
                        "metadata": {"source": "pymupdf"}
                    })

        doc.close()
        return elements