from typing import Dict, List, Optional

from detector.pdf_classifier import PDFClassifier
from router.extraction_router import ExtractionRouter
from validator.text_validator import TextValidator
from chunking.semantic_chunker import SemanticChunker
from chunking.layout_chunker import LayoutChunker
from extractor.pdf.layout_aware_extractor import LayoutAwareExtractor
from embedding.embedder import Embedder
from utils.logger import get_logger
from utils.utils import text_parser

logger = get_logger(__name__)

embedder = Embedder()

class RAGPipeline:
    def __init__(self, use_layout_aware: bool = False) -> None:
        self.classifier = PDFClassifier()
        self.router = ExtractionRouter()
        self.validator = TextValidator()
        self.use_layout_aware = use_layout_aware
        
        if use_layout_aware:
            self.chunker = LayoutChunker(
                chunk_size=1000,
                chunk_overlap=100,
                respect_hierarchy=True
            )
        else:
            self.chunker = SemanticChunker()
        
        self._layout_analyzer = None

    def run(self, file_path: str) -> Dict[str, object]:
        logger.info(f'Starting pipeline for: {file_path}')
        logger.info(f'Layout-aware mode: {self.use_layout_aware}')

        pdf_type = self._detect(file_path)
        
        if self.use_layout_aware:
            extractor = LayoutAwareExtractor(file_path, preserve_layout=True)
            logger.info(f'Using layout-aware extractor')
        else:
            extractor = self._route(pdf_type, file_path)
            
        raw_text = self._extract(extractor, file_path)
        clean_text = self._validate(raw_text)
        
        # Use layout-aware chunking if available
        result = {
            'file_path': file_path,
            'pdf_type': pdf_type,
            'status': 'success',
            'layout_aware': self.use_layout_aware,
        }

        if self.use_layout_aware and hasattr(extractor, 'get_layout_pages'):
            # Use layout elements for chunking to preserve page numbers
            layout_pages = extractor.get_layout_pages()
            if layout_pages:
                result['num_pages'] = len(layout_pages)
                
                # Extract all layout elements (text + tables mixed)
                all_elements = []
                for page in layout_pages:
                    all_elements.extend(page.elements)
                
                # Count tables for metadata
                tables = [elem for elem in all_elements if elem.type == 'table']
                result['tables_detected'] = len(tables)
                
                # Use layout-aware chunking with page information (tables stay in stream)
                page_width = layout_pages[0].page_width if layout_pages else 1000
                page_height = layout_pages[0].page_height if layout_pages else 1000
                chunks = self.chunker.chunk_with_layout(
                    all_elements, page_width, page_height
                )
                result['chunks'] = chunks
                result['num_chunks'] = len(chunks)
                logger.info(f'Created {len(chunks)} layout-aware chunks with page numbers (tables in stream)')
                logger.info(f'Embedding generation started .....')
                texts = [text_parser(chunk.content) for chunk in chunks]
                result['embeddings'] = embedder.embed(texts)
                logger.info(f'Generated embeddings length : {len(result["embeddings"][0])} for first chunk')
                logger.info(f'Embedding generation completed')
        else:
            # Fall back to text-based chunking
            chunks = self._chunk(clean_text, file_path)
            result['chunks'] = chunks
            result['num_chunks'] = len(chunks)
            result['embeddings'] = embedder.embed([chunk.content for chunk in chunks])
        return result

    def _detect(self, file_path: str) -> str:
        pdf_type = self.classifier.classify(file_path)
        logger.info(f'Detected PDF type: {pdf_type}')
        return pdf_type

    def _route(self, pdf_type: str, file_path: str):
        extractor = self.router.get_extractor(pdf_type, file_path)
        logger.info(f'Using extractor: {extractor.__class__.__name__}')
        return extractor

    def _extract(self, extractor, file_path: str) -> str:
        text = extractor.extract()

        if not text or len(text.strip()) < 50:
            logger.warning('Low text extracted, triggering fallback scanned extraction')
            extractor = self.router.get_extractor('scanned', file_path)
            text = extractor.extract()

        return text or ''

    def _validate(self, text: str) -> str:
        if not self.validator.is_valid(text):
            logger.warning('Text validation failed, attempting cleanup')
            return self.validator.clean(text)

        return text

    def _chunk(self, text: str, file_path: Optional[str] = None) -> List:
        """
        Chunk text using either layout-aware or semantic chunking.
        
        Args:
            text: The text to chunk
            file_path: Optional file path for layout-aware extraction metadata
            
        Returns:
            List of chunks (Chunk objects for layout-aware, strings for semantic)
        """
        if self.use_layout_aware:
            if isinstance(self.chunker, LayoutChunker):
                chunks = self.chunker.chunk(text, metadata={'source': file_path})
                logger.info(f'Created {len(chunks)} layout-aware chunks')
                return chunks
        
        chunks = self.chunker.chunk(text)
        logger.info(f'Created {len(chunks)} semantic chunks')
        return chunks
