"""
Production-grade RAG ingestion pipeline

Flow:
PDF → Detect → Route → Extract → Validate → Chunk → Embed → Store
"""

from typing import List, Dict

# Detector
from detector.pdf_classifier import PDFClassifier

# # Router
# from router.extraction_router import ExtractionRouter

# # Validator
# from validator.text_validator import TextValidator

# # Chunking
# from chunking.semantic_chunker import SemanticChunker

# # Embedding
# from embedding.embedder import Embedder

# # Storage
# from storage.faiss_store import FAISSVectorStore

# Logger (important in production)
from utils.logger import get_logger


logger = get_logger(__name__)


class RAGPipeline:
    def __init__(self):
        # Core components
        self.classifier = PDFClassifier()
        # self.router = ExtractionRouter()
        # self.validator = TextValidator()
        # self.chunker = SemanticChunker()
        # self.embedder = Embedder()
        # self.vector_store = FAISSVectorStore()

    # -----------------------------
    # Main Entry Point
    # -----------------------------
    def run(self, file_path: str) -> Dict:
        logger.info(f"Starting pipeline for: {file_path}")

        # 1. Detect PDF type
        pdf_type = self._detect(file_path)

        # # 2. Route extractor
        # extractor = self._route(pdf_type)

        # # 3. Extract text
        # raw_text = self._extract(extractor, file_path)

        # # 4. Validate text
        # clean_text = self._validate(raw_text)

        # # 5. Chunk text
        # chunks = self._chunk(clean_text)

        # # 6. Generate embeddings
        # embeddings = self._embed(chunks)

        # # 7. Store in vector DB
        # self._store(chunks, embeddings)

        # logger.info("✅ Pipeline completed successfully")

        # return {
        #     "pdf_type": pdf_type,
        #     "num_chunks": len(chunks),
        #     "status": "success"
        # }
        return {
            "pdf_type": pdf_type,
            "status": "success"
        }

    # -----------------------------
    # Individual Steps
    # -----------------------------

    def _detect(self, file_path: str) -> str:
        pdf_type = self.classifier.classify(file_path)
        logger.info(f"Detected PDF type: {pdf_type}")
        return pdf_type

    def _route(self, pdf_type: str):
        extractor = self.router.get_extractor(pdf_type)
        logger.info(f"Using extractor: {extractor.__class__.__name__}")
        return extractor

    def _extract(self, extractor, file_path: str) -> str:
        text = extractor.extract(file_path)

        if not text or len(text.strip()) < 50:
            logger.warning("Low text extracted, triggering fallback OCR")

            # fallback OCR
            extractor = self.router.get_extractor("scanned")
            text = extractor.extract(file_path)

        return text

    def _validate(self, text: str) -> str:
        if not self.validator.is_valid(text):
            logger.warning("Text validation failed, attempting cleanup")
            text = self.validator.clean(text)

        return text

    def _chunk(self, text: str) -> List[str]:
        chunks = self.chunker.chunk(text)
        logger.info(f"✂️ Created {len(chunks)} chunks")
        return chunks

    def _embed(self, chunks: List[str]):
        embeddings = self.embedder.embed(chunks)
        logger.info(f"🧬 Generated embeddings")
        return embeddings

    def _store(self, chunks: List[str], embeddings):
        self.vector_store.add(chunks, embeddings)
        logger.info("Stored embeddings in vector DB")  