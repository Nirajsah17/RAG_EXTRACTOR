from extractor.extractor import PdfExtractor

class ExtractionRouter(self):
  def __init__(self):
    pass
  
  def _route(self, pdf_type: str):
    if pdf_type == "scanned":
      return pass
    elif pdf_type == "digital":
      return PdfExtractor
    elif pdf_type == "mixed":
      return pass
    elif pdf_type == "scanned+ocr":
      return pass
    else:
      raise ValueError(f"Unsupported PDF type: {pdf_type}")