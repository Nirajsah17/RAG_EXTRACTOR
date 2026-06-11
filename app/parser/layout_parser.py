import fitz
from models.document import DocumentNode

def extract_layout(pdf_path: str):
    doc = fitz.open(pdf_path)
    nodes = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        for block_id, block in enumerate(blocks):
            if "lines" not in block:
                continue

            text = ""
            max_font = 0
            is_bold = False

            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"] + " "
                    max_font = max(max_font, span["size"])
                    is_bold = is_bold or ("bold" in span["font"].lower())

            text = text.strip()

            if text:
                nodes.append(DocumentNode(
                    doc_id=pdf_path,
                    page=page_num,
                    block_id=block_id,
                    type="text",
                    text=text,
                    bbox=block["bbox"],
                    metadata={
                        "font_size": max_font,
                        "is_heading": max_font >= 13
                    }
                ))

    return nodes