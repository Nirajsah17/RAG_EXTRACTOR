class TesseractOcrExtractor:
    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path

    def extract(self) -> str:
        raise NotImplementedError('Tesseract OCR extraction is not implemented in this branch.')
