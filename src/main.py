import argparse
from pathlib import Path

from ingestion.orchestrator import process_path
from ingestion.pipeline import RAGPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description='RAG Ingestion Pipeline')
    parser.add_argument(
        'path',
        type=str,
        help='Path to a PDF file or a folder containing PDFs',
    )
    parser.add_argument('--log_level', default='INFO', help='Logging level')
    parser.add_argument('--log_dir', default='logs', help='Directory for log files')
    parser.add_argument(
        '--output_dir',
        default='data/processed',
        help='Directory to save JSON results (default: data/processed)',
    )
    parser.add_argument(
        '--save_results',
        type=bool,
        default=True,
        help='Save extraction results to JSON files (default: True)',
    )

    args = parser.parse_args()
    input_path = Path(args.path)

    pipeline = RAGPipeline(use_layout_aware=True)
    results = process_path(
        input_path,
        pipeline,
        save_results=args.save_results,
        output_dir=args.output_dir,
    )


if __name__ == '__main__':
    main()
