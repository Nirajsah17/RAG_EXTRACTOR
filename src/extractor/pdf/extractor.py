from typing import List

from .base_extractor import BaseExtractor


class PdfExtractor:
    def __init__(self, pdf_path: str, extractors: List[BaseExtractor]) -> None:
        self.pdf_path = pdf_path
        self.extractors = extractors

    def extract(self) -> str:
        extracted_fragments = []

        for extractor in self.extractors:
            try:
                extracted_fragments.append(extractor.extract())
            except Exception as exc:
                print(f'Extractor failed: {exc}')

        return '\n\n'.join(fragment.strip() for fragment in extracted_fragments if fragment)
