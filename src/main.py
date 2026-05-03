import argparse
from pathlib import Path
from ingestion.pipeline import RAGPipeline

parser = argparse.ArgumentParser(description="RAG Ingestion Pipeline")

parser.add_argument(
    "path",
    type=str,
    help="Path to a PDF file or a folder containing PDFs",
)

parser.add_argument("--log_level", default="INFO")
parser.add_argument("--log_dir", default="logs")

def process_path(path: Path, pipeline: RAGPipeline):
  if path.is_file():
    print(f"Processing file: {path}")
    return [pipeline.run(str(path))]

  elif path.is_dir():
    print(f"Processing folder: {path}")
    results = []

    for pdf in path.rglob("*.pdf"):
      print(f"Processing: {pdf}")
      results.append(pipeline.run(str(pdf)))

    return results

  else:
    raise ValueError(f"Invalid path: {path}")

if __name__ == "__main__":
    args = parser.parse_args()

    input_path = Path(args.path)

    pipeline = RAGPipeline()

    results = process_path(input_path, pipeline)

    print("\nFinal Results:")
    for r in results:
        print(r)