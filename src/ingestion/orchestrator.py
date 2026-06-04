from pathlib import Path
from typing import List, Optional

from ingestion.pipeline import RAGPipeline
from storage.result_saver import ResultSaver


def process_path(
    path: Path,
    pipeline: RAGPipeline,
    save_results: bool = True,
    output_dir: str = 'data/processed',
) -> List[dict]:
    """
    Process PDF file(s) and optionally save results to JSON.
    
    Args:
        path: Path to PDF file or directory containing PDFs
        pipeline: RAGPipeline instance to process files
        save_results: Whether to save results to JSON files
        output_dir: Directory to save JSON results
        
    Returns:
        List of extraction result dictionaries
    """
    saver = ResultSaver(output_dir) if save_results else None
    results = []

    if path.is_file():
        print(f'Processing file: {path}')
        result = pipeline.run(str(path))
        results.append(result)
        if save_results and saver:
            saver.save_result(result)
        return results

    if path.is_dir():
        print(f'Processing folder: {path}')

        for pdf_path in sorted(path.rglob('*.pdf')):
            print(f'Processing: {pdf_path}')
            result = pipeline.run(str(pdf_path))
            results.append(result)
            if save_results and saver:
                saver.save_result(result)

        # Also save combined results if processing multiple files
        if save_results and saver and len(results) > 1:
            print(f'Saving combined results for {len(results)} files...')
            saver.save_combined_results(results, batch_name='extraction_batch')

        return results

    raise ValueError(f'Invalid path: {path}')
