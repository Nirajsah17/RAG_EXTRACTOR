import pdfplumber
from base_extractor import BaseExtractor

class PdfPlumberExtractor(BaseExtractor):
  def __init__(self, pdf_path: str):
      self.pdf_path = pdf_path

  def extract(self):
    elements = []
    with pdfplumber.open(self.pdf_path) as pdf:
      for page_num, page in enumerate(pdf.pages):
        words = page.extract_words()
        for w in words:
          elements.append({
              "type": "text",
              "content": w["text"],
              "page": page_num,
              "bbox": (w["x0"], w["top"], w["x1"], w["bottom"]),
              "metadata": {"source": "pdfplumber"}
          })

        for table in page.extract_tables():
          elements.append({
              "type": "table",
              "content": table,
              "page": page_num,
              "bbox": None,
              "metadata": {"source": "pdfplumber"}
          })

    return elements