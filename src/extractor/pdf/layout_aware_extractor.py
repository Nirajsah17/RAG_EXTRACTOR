from typing import Optional, List
from .base_extractor import BaseExtractor
from ..layout_analyzer import LayoutAnalyzer, LayoutPage


class LayoutAwareExtractor(BaseExtractor):
    """
    Extract text from PDFs while preserving layout and structure information.
    Uses layout analysis to detect tables, headings, and maintain document hierarchy.
    """

    def __init__(self, pdf_path: str, preserve_layout: bool = True):
        self.pdf_path = pdf_path
        self.preserve_layout = preserve_layout
        self._layout_analyzer: Optional[LayoutAnalyzer] = None
        self._layout_pages: Optional[List[LayoutPage]] = None

    def extract(self) -> str:
        """Extract text with layout preservation."""
        try:
            import pdfplumber
        except ImportError as exc:
            raise ImportError(
                'pdfplumber is required for LayoutAwareExtractor. Install it with `pip install pdfplumber`.'
            ) from exc

        if self.preserve_layout:
            return self._extract_with_layout()
        else:
            return self._extract_basic()

    def _extract_with_layout(self) -> str:
        """Extract using layout analysis."""
        analyzer = LayoutAnalyzer(self.pdf_path)
        self._layout_pages = analyzer.analyze()
        self._layout_analyzer = analyzer

        return analyzer.get_structural_text(preserve_hierarchy=True)

    def _extract_basic(self) -> str:
        """Fallback basic extraction."""
        try:
            import pdfplumber
        except ImportError as exc:
            raise ImportError(
                'pdfplumber is required for LayoutAwareExtractor. Install it with `pip install pdfplumber`.'
            ) from exc

        text_parts = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ''
                if page_text:
                    text_parts.append(page_text)

        return '\n\n'.join(text_parts).strip()

    def get_layout_pages(self) -> Optional[List[LayoutPage]]:
        """Get parsed layout pages. Runs extract() if not already done."""
        if self._layout_pages is None:
            self.extract()
        return self._layout_pages

    def get_layout_analyzer(self) -> Optional[LayoutAnalyzer]:
        """Get the layout analyzer instance."""
        if self._layout_analyzer is None:
            self._layout_analyzer = LayoutAnalyzer(self.pdf_path)
            if self._layout_pages is None:
                self._layout_pages = self._layout_analyzer.analyze()
        return self._layout_analyzer
