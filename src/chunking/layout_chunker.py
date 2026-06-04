from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a chunk with metadata."""
    content: str
    chunk_id: int
    start_pos: int
    end_pos: int
    hierarchy_level: int = 0
    source_type: str = 'text'  # 'text', 'table', 'mixed'
    page_num: Optional[int] = None
    metadata: Optional[Dict] = None


class LayoutChunker:
    """Chunks text while respecting layout and document structure."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        respect_hierarchy: bool = True,
        min_chunk_size: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.respect_hierarchy = respect_hierarchy
        self.min_chunk_size = min_chunk_size

    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """Chunk text while preserving structure and meaning."""
        if not text or len(text.strip()) < self.min_chunk_size:
            return [
                Chunk(
                    content=text,
                    chunk_id=0,
                    start_pos=0,
                    end_pos=len(text),
                    metadata=metadata,
                )
            ]

        # Split by logical structure markers
        sections = self._split_by_structure(text)
        chunks = []
        chunk_id = 0

        for section, section_level in sections:
            section_chunks = self._chunk_section(
                section, section_level, chunk_id, metadata
            )
            chunks.extend(section_chunks)
            chunk_id += len(section_chunks)

        return chunks

    def _split_by_structure(
        self, text: str
    ) -> List[Tuple[str, int]]:
        """Split text by heading markers (##, ###) while respecting hierarchy."""
        lines = text.split('\n')
        sections = []
        current_section = []
        current_level = 0

        for line in lines:
            # Detect heading level from markdown markers
            level = self._detect_heading_level(line)

            if level > 0:
                # Save current section if not empty
                if current_section:
                    section_text = '\n'.join(current_section).strip()
                    if len(section_text) >= self.min_chunk_size:
                        sections.append((section_text, current_level))

                current_section = [line]
                current_level = level
            else:
                current_section.append(line)

        # Add final section
        if current_section:
            section_text = '\n'.join(current_section).strip()
            if len(section_text) >= self.min_chunk_size:
                sections.append((section_text, current_level))

        return sections if sections else [(text, 0)]

    def _detect_heading_level(self, line: str) -> int:
        """Detect heading level from markdown or heuristics."""
        stripped = line.lstrip()
        if stripped.startswith('##'):
            if stripped.startswith('###'):
                return 3
            return 2
        return 0

    def _chunk_section(
        self,
        section: str,
        hierarchy_level: int,
        start_chunk_id: int,
        metadata: Optional[Dict],
    ) -> List[Chunk]:
        """Chunk a section of text, respecting logical boundaries."""
        # Try to split by sentence first
        sentences = self._split_sentences(section)

        if not sentences:
            return [
                Chunk(
                    content=section,
                    chunk_id=start_chunk_id,
                    start_pos=0,
                    end_pos=len(section),
                    hierarchy_level=hierarchy_level,
                    metadata=metadata,
                )
            ]

        chunks = []
        current_chunk = []
        current_length = 0
        chunk_id = start_chunk_id
        start_pos = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            # Check if adding this sentence would exceed chunk size
            if (
                current_length + sentence_length > self.chunk_size
                and current_chunk
            ):
                # Save current chunk
                chunk_text = ' '.join(current_chunk).strip()
                if len(chunk_text) >= self.min_chunk_size:
                    chunk = Chunk(
                        content=chunk_text,
                        chunk_id=chunk_id,
                        start_pos=start_pos,
                        end_pos=start_pos + len(chunk_text),
                        hierarchy_level=hierarchy_level,
                        metadata=metadata,
                    )
                    chunks.append(chunk)
                    chunk_id += 1

                    # Calculate overlap
                    overlap_sentences = self._get_overlap_sentences(
                        current_chunk
                    )
                    current_chunk = overlap_sentences + [sentence]
                    current_length = sum(len(s) for s in current_chunk)
                    start_pos += len(chunk_text) - len(' '.join(overlap_sentences))
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk).strip()
            if len(chunk_text) >= self.min_chunk_size:
                chunk = Chunk(
                    content=chunk_text,
                    chunk_id=chunk_id,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    hierarchy_level=hierarchy_level,
                    metadata=metadata,
                )
                chunks.append(chunk)

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling common cases."""
        import re

        # Preserve whitespace while splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """Get sentences for overlap to maintain context."""
        if not sentences:
            return []

        # Calculate how many sentences fit in overlap window
        overlap_length = 0
        overlap_sentences = []

        for sentence in reversed(sentences):
            if overlap_length + len(sentence) <= self.chunk_overlap:
                overlap_sentences.insert(0, sentence)
                overlap_length += len(sentence)
            else:
                break

        return overlap_sentences

    def chunk_with_layout(
        self,
        layout_elements: List,
        page_width: float,
        page_height: float,
    ) -> List[Chunk]:
        """
        Chunk using layout elements (requires layout_analyzer.py LayoutElement objects).
        
        Args:
            layout_elements: List of LayoutElement objects from LayoutAnalyzer
            page_width: Width of the page
            page_height: Height of the page
            
        Returns:
            List of Chunk objects with layout awareness
        """
        chunks = []
        chunk_id = 0

        # Group elements by page
        for element in layout_elements:
            # Create chunks respecting element boundaries
            if element.type == 'table':
                # Tables should not be split across chunks
                chunk = Chunk(
                    content=element.content,
                    chunk_id=chunk_id,
                    start_pos=0,
                    end_pos=len(element.content),
                    hierarchy_level=element.hierarchy_level,
                    source_type='table',
                    page_num=element.page_num,
                    metadata={
                        'bbox': element.bbox,
                        'font_size': element.font_size,
                        'is_bold': element.is_bold,
                    },
                )
                chunks.append(chunk)
                chunk_id += 1
            else:
                # For text elements, chunk if too large
                if len(element.content) > self.chunk_size:
                    element_chunks = self.chunk(
                        element.content,
                        metadata={
                            'bbox': element.bbox,
                            'font_size': element.font_size,
                            'is_bold': element.is_bold,
                            'page_num': element.page_num,
                        },
                    )
                    for elem_chunk in element_chunks:
                        elem_chunk.chunk_id = chunk_id
                        elem_chunk.source_type = 'text'
                        elem_chunk.page_num = element.page_num
                        chunks.append(elem_chunk)
                        chunk_id += 1
                else:
                    chunk = Chunk(
                        content=element.content,
                        chunk_id=chunk_id,
                        start_pos=0,
                        end_pos=len(element.content),
                        hierarchy_level=element.hierarchy_level,
                        source_type='text',
                        page_num=element.page_num,
                        metadata={
                            'bbox': element.bbox,
                            'font_size': element.font_size,
                            'is_bold': element.is_bold,
                        },
                    )
                    chunks.append(chunk)
                    chunk_id += 1

        return chunks
