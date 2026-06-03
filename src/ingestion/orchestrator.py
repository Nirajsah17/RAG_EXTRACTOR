from pathlib import Path
from typing import List

from ingestion.pipeline import RAGPipeline


def process_path(path: Path, pipeline: RAGPipeline) -> List[dict]:
    if path.is_file():
        print(f'Processing file: {path}')
        return [pipeline.run(str(path))]

    if path.is_dir():
        print(f'Processing folder: {path}')
        results = []

        for pdf_path in sorted(path.rglob('*.pdf')):
            print(f'Processing: {pdf_path}')
            results.append(pipeline.run(str(pdf_path)))

        return results

    raise ValueError(f'Invalid path: {path}')
