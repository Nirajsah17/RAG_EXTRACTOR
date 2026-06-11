import fitz
from models.document import DocumentNode

def extract_tables(pdf_path: str):
    doc = fitz.open(pdf_path)
    nodes = []

    for page_num, page in enumerate(doc, start=1):
        tables = page.find_tables()

        for i, table in enumerate(tables):
            nodes.append(DocumentNode(
                doc_id=pdf_path,
                page=page_num,
                block_id=i,
                type="table",
                text=str(table.extract()),
                bbox=table.bbox,
                metadata={}
            ))

    return nodes