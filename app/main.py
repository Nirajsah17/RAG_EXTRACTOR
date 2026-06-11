from config import load_config
from parser.builder import build_document
# from chunker.chunker import chunk_nodes
from chunker.chunker import chunk_with_headings
from utils.logger import get_logger

from utils.file_utils import ensure_dir
from pathlib import Path
import json

def main():
    logger = get_logger()
    config = load_config()

    ensure_dir(config.output_dir)

    pdf_path = Path(config.input_dir) / "kehs102.pdf"

    logger.info("Parsing PDF...")

    nodes = build_document(str(pdf_path), config)

    logger.info(f"Total nodes: {len(nodes)}")

    # chunks = chunk_nodes(nodes, config.chunk_size)
    # chunks = chunk_nodes(nodes, config)
    # chunks = chunk_nodes(nodes, config.chunk_size, config.chunk_overlap)
    chunks = chunk_with_headings(
        nodes,
        config.chunk_size,
        config.chunk_overlap
    )

    logger.info(f"Total chunks: {len(chunks)}")

    output_file = Path(config.output_dir) / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            [node.to_dict() for node in nodes],
            f,
            indent=2,
            ensure_ascii=False
        )

    logger.info(f"Saved to {output_file}")

if __name__ == "__main__":
    main()