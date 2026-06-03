from .base_extractor import BaseExtractor


class PdfPlumberExtractor(BaseExtractor):
    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path

    def extract(self) -> str:
        try:
            import pdfplumber
        except ImportError as exc:
            raise ImportError('pdfplumber is required for PdfPlumberExtractor. Install it with `pip install pdfplumber`.') from exc

        text_parts = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ''
                if page_text:
                    text_parts.append(page_text)

        return '\n\n'.join(text_parts).strip()
