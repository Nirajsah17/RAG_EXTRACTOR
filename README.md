doc-rag/
├── data/                     # raw + processed files
│   ├── raw/
│   ├── processed/
│
├── src/
│   ├── ingestion/           # entry point for RAG pipeline
│   │   ├── pipeline.py
│   │   ├── orchestrator.py
│
│   ├── extractor/           # pure extraction logic
│   │   ├── pdf/
│   │   │   ├── pymupdf_extractor.py
│   │   │   ├── pdfplumber_extractor.py
│   │   │   ├── metadata.py
│   │   │
│   │   ├── ocr/
│   │   │   ├── tesseract_ocr.py
│
│   ├── detector/            # PDF type detection
│   │   ├── pdf_classifier.py
│
│   ├── validator/           # quality checks
│   │   ├── text_validator.py
│   │   ├── ocr_validator.py
│
│   ├── router/              # decision engine
│   │   ├── extraction_router.py
│
│   ├── chunking/            # RAG chunking logic
│   │   ├── semantic_chunker.py
│   │   ├── layout_chunker.py
│
│   ├── embedding/           # vectorization
│   │   ├── embedder.py
│
│   ├── storage/             # vector DB
│   │   ├── faiss_store.py
│   │   ├── pinecone_store.py
│
│   ├── utils/
│   │   ├── logger.py
│   │   ├── config.py
│
│   ├── main.py              # CLI / entrypoint










def run_pipeline(file_path):
    pdf_type = classify_pdf(file_path)
    
    extractor = route_extractor(pdf_type)
    
    raw_text = extractor.extract(file_path)
    
    validated_text = validate_text(raw_text)
    
    chunks = chunk_text(validated_text)
    
    store_embeddings(chunks)