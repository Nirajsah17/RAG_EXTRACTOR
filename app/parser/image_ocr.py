import fitz
import io
from PIL import Image
import pytesseract
from models.document import DocumentNode

def extract_images(pdf_path: str):
    doc = fitz.open(pdf_path)
    nodes = []

    for page_num, page in enumerate(doc, start=1):
        images = page.get_images(full=True)

        for img_id, img in enumerate(images):
            xref = img[0]
            base = doc.extract_image(xref)

            image = Image.open(io.BytesIO(base["image"]))
            text = pytesseract.image_to_string(image)

            if text.strip():
                nodes.append(DocumentNode(
                    doc_id=pdf_path,
                    page=page_num,
                    block_id=img_id,
                    type="image",
                    text=text.strip(),
                    bbox=None,
                    metadata={"source": "ocr"}
                ))

    return nodes