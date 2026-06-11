import argparse
from pathlib import Path

# from ingestion.orchestrator import process_path
# from ingestion.pipeline import RAGPipeline
from pipeline import ExtractionPipeline

# from fio.reader import is_file_exist, is_dir_exist, ispdf, is_dir_contains_pdf


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

    # if not is_file_exist(input_path) and not is_dir_exist(input_path):
    #     print(f"Error: Path does not exist: {input_path}")
    #     return
    # if is_file_exist(input_path) and not ispdf(input_path):
    #     print(f"Error: File is not a PDF: {input_path}")
    #     return
    # if is_dir_exist(input_path) and not is_dir_contains_pdf(input_path):
    #     print(f"Error: Directory does not contain any PDF files: {input_path}")
    #     return

    print(f"Processing path: {input_path} \n")
    
    print(f"Log level: {args.log_level} \n")
    
    print(f"Log directory: {args.log_dir} \n")
    
    print(f"Output directory: {args.output_dir} \n")
    
    print(f"Save results: {args.save_results} \n")

    # pipeline = RAGPipeline(use_layout_aware=True)
    # results = process_path(
    #     input_path,
    #     pipeline,
    #     save_results=args.save_results,
    #     output_dir=args.output_dir,
    # )
    
    pipeline = ExtractionPipeline(
        input_path =  input_path,
        output_path =  args.output_dir
    )
    pipeline.run()


if __name__ == '__main__':
    main()
