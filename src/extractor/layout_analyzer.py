from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class LayoutElement:
    """Represents a layout element in a PDF page."""
    type: str  # 'text', 'table', 'image', 'heading', 'list'
    content: str
    bbox: Tuple[float, float, float, float]  # (x0, top, x1, bottom)
    page_num: int
    font_size: Optional[float] = None
    is_bold: bool = False
    hierarchy_level: int = 0  # 0 for page, 1 for section, 2 for subsection, etc.


@dataclass
class LayoutPage:
    """Represents a parsed page with layout information."""
    page_num: int
    elements: List[LayoutElement]
    page_width: float
    page_height: float
    text_content: str


class LayoutAnalyzer:
    """Analyzes PDF layout and structure."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pages: List[LayoutPage] = []

    def analyze(self) -> List[LayoutPage]:
        """Analyze PDF and extract layout information using pdfplumber."""
        try:
            import pdfplumber
        except ImportError as exc:
            raise ImportError(
                'pdfplumber is required for layout analysis. Install it with `pip install pdfplumber`.'
            ) from exc

        self.pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                layout_page = self._analyze_page(page, page_num)
                self.pages.append(layout_page)

        return self.pages

    def _analyze_page(self, page, page_num: int) -> LayoutPage:
        """Analyze a single page for layout elements."""
        elements = []
        text_content = ""

        # Extract tables
        tables = page.extract_tables()
        if tables:
            for table in tables:
                table_text = self._format_table(table)
                elements.append(
                    LayoutElement(
                        type='table',
                        content=table_text,
                        bbox=self._get_table_bbox(table),
                        page_num=page_num,
                        hierarchy_level=1,
                    )
                )
                text_content += table_text + "\n\n"

        # Extract text with position information
        text_objects = page.extract_words()
        if text_objects:
            elements.extend(
                self._group_text_by_position(text_objects, page_num)
            )
            text_content += page.extract_text() or ""

        # Extract lines (for structure detection)
        lines = page.lines
        if lines:
            self._detect_structure(elements, lines, page_num)

        return LayoutPage(
            page_num=page_num,
            elements=elements,
            page_width=page.width,
            page_height=page.height,
            text_content=text_content.strip(),
        )

    def _group_text_by_position(
        self, text_objects: List[Dict], page_num: int
    ) -> List[LayoutElement]:
        """Group text objects by their position (lines, paragraphs)."""
        if not text_objects:
            return []

        # Sort by top position and then by left position
        sorted_objects = sorted(text_objects, key=lambda x: (x['top'], x['x0']))

        elements = []
        current_line = []
        current_top = sorted_objects[0]['top']
        line_threshold = 5  # pixels

        for obj in sorted_objects:
            # Check if this object is on a new line
            if abs(obj['top'] - current_top) > line_threshold:
                if current_line:
                    elements.append(
                        self._create_text_element(current_line, page_num)
                    )
                current_line = []
                current_top = obj['top']

            current_line.append(obj)

        # Add the last line
        if current_line:
            elements.append(self._create_text_element(current_line, page_num))

        return elements

    def _create_text_element(
        self, text_objects: List[Dict], page_num: int
    ) -> LayoutElement:
        """Create a text element from grouped text objects."""
        text = ' '.join(obj['text'] for obj in text_objects)
        x0 = min(obj['x0'] for obj in text_objects)
        top = min(obj['top'] for obj in text_objects)
        x1 = max(obj['x1'] for obj in text_objects)
        bottom = max(obj['bottom'] for obj in text_objects)

        # Estimate font size and detect bold - handle missing 'size' key
        sizes = [obj.get('size', 12) for obj in text_objects]
        avg_size = sum(sizes) / len(sizes) if sizes else 12
        is_bold = any(obj.get('size', 0) > avg_size * 1.2 for obj in text_objects)
        hierarchy_level = self._estimate_hierarchy(text, avg_size)

        return LayoutElement(
            type='text',
            content=text,
            bbox=(x0, top, x1, bottom),
            page_num=page_num,
            font_size=avg_size,
            is_bold=is_bold,
            hierarchy_level=hierarchy_level,
        )

    def _estimate_hierarchy(self, text: str, font_size: float) -> int:
        """Estimate hierarchy level based on font size and text patterns."""
        # Heuristic: larger font often indicates heading
        if font_size > 14:
            return 1  # Likely a heading
        elif font_size > 12:
            if text.isupper() or len(text) < 50:
                return 1
            return 2
        elif font_size < 10:
            return 3  # Small font, likely body or list
        return 2

    def _format_table(self, table: List[List[str]]) -> str:
        """Format table data as structured text."""
        if not table:
            return ""

        formatted_rows = []
        for row in table:
            formatted_row = ' | '.join(cell or '' for cell in row)
            formatted_rows.append(formatted_row)

        return '\n'.join(formatted_rows)

    def _get_table_bbox(self, table: List[List[str]]) -> Tuple[float, float, float, float]:
        """Get bounding box of a table (approximation)."""
        # Placeholder: actual implementation would need table cell positions
        return (0, 0, 1000, len(table) * 20)

    def _detect_structure(
        self, elements: List[LayoutElement], lines: List[Dict], page_num: int
    ) -> None:
        """Detect structural elements like sections, columns."""
        # This is a placeholder for more sophisticated structure detection
        # Could be extended to detect multi-column layouts, sections, etc.
        pass

    def get_structural_text(self, preserve_hierarchy: bool = True) -> str:
        """Get complete text content preserving structure."""
        if not self.pages:
            self.analyze()

        full_text = []

        for page in self.pages:
            # Sort elements by position (top to bottom, left to right)
            sorted_elements = sorted(page.elements, key=lambda e: (e.bbox[1], e.bbox[0]))

            for element in sorted_elements:
                if preserve_hierarchy and element.hierarchy_level == 1:
                    # Add extra spacing for headings
                    full_text.append(f"\n## {element.content}\n")
                elif preserve_hierarchy and element.hierarchy_level == 2:
                    full_text.append(f"\n### {element.content}\n")
                else:
                    full_text.append(element.content)

                if element.type == 'table':
                    full_text.append('\n')

            full_text.append('\n---\n')  # Page separator

        return ''.join(full_text)
