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

    args = parser.parse_args()
    input_path = Path(args.path)

    pipeline = RAGPipeline()
    results = process_path(input_path, pipeline)

    print('\nFinal Results:')
    for item in results:
        print(item)


if __name__ == '__main__':
    main()
