
from pdfplumber_extract import PdfPlumberExtractor
from pymupdf_extractor import PyMuPDFExtractor

class PdfExtractor:
  def __init__(self, extractors):
      self.extractors = extractors

  def _extract(self):
    all_elements = []

    for extractor in self.extractors:
        try:
            data = extractor.extract()
            all_elements.extend(data)
        except Exception as e:
            print(f"Extractor failed: {e}")

    all_elements.sort(
        key=lambda x: (
            x["page"],
            x["bbox"][1] if x["bbox"] else 0
        )
    )

  return all_elements

def pdf_extractor(pdf_path):
  
  extractor = PdfExtractor([
      PyMuPDFExtractor(pdf_path),
      PdfPlumberExtractor(pdf_path)
  ])

    elements = extractor.extract()

    # for el in elements[:10]:
    #     print(el)