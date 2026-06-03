from .base_extractor import BaseExtractor


class PyMuPDFExtractor(BaseExtractor):
    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path

    def extract(self) -> str:
        try:
            import fitz
        except ImportError as exc:
            raise ImportError('PyMuPDF is required for PyMuPDFExtractor. Install it with `pip install pymupdf`.') from exc

        text_parts = []
        with fitz.open(self.pdf_path) as doc:
            for page in doc:
                text_parts.append(page.get_text())

        return '\n\n'.join(text_parts).strip()
