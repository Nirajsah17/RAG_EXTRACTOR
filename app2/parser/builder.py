from parser.layout_parser import extract_layout
from parser.image_ocr import extract_images
from parser.table_parser import extract_tables

def build_document(pdf_path: str, config):
    nodes = []

    nodes += extract_layout(pdf_path)

    if config.enable_ocr:
        nodes += extract_images(pdf_path)

    if config.enable_tables:
        nodes += extract_tables(pdf_path)

    nodes.sort(key=lambda x: (x.page, x.block_id))

    return nodes