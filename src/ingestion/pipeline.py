from typing import Dict

from detector.pdf_classifier import PDFClassifier
from router.extraction_router import ExtractionRouter
from validator.text_validator import TextValidator
from chunking.semantic_chunker import SemanticChunker
from utils.logger import get_logger

logger = get_logger(__name__)


class RAGPipeline:
    def __init__(self) -> None:
        self.classifier = PDFClassifier()
        self.router = ExtractionRouter()
        self.validator = TextValidator()
        self.chunker = SemanticChunker()

    def run(self, file_path: str) -> Dict[str, object]:
        logger.info(f'Starting pipeline for: {file_path}')

        pdf_type = self._detect(file_path)
        extractor = self._route(pdf_type, file_path)
        raw_text = self._extract(extractor, file_path)
        clean_text = self._validate(raw_text)
        chunks = self._chunk(clean_text)

        return {
            'file_path': file_path,
            'pdf_type': pdf_type,
            'num_chunks': len(chunks),
            'status': 'success',
        }

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

    def _chunk(self, text: str):
        chunks = self.chunker.chunk(text)
        logger.info(f'Created {len(chunks)} chunks')
        return chunks
