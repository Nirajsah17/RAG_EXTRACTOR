import fitz

class PDFClassifier:
    def __init__(self):
        pass

    def classify(self, file_path: str):
        doc = fitz.open(file_path)

        total_pages = len(doc)
        image_pages = 0
        text_pages = 0
        ocr_like_pages = 0

        for page in doc:
            blocks = page.get_text("dict")["blocks"]

            text_area = 0
            image_area = 0
            page_area = page.rect.width * page.rect.height

            has_text = False
            has_image = False

            for b in blocks:
                if b["type"] == 0:
                    has_text = True
                    for line in b["lines"]:
                        for span in line["spans"]:
                            bbox = span["bbox"]
                            text_area += (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

                elif b["type"] == 1:
                    has_image = True
                    bbox = b["bbox"]
                    image_area += (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

            if has_image and not has_text:
                image_pages += 1

            elif has_text:
                text_pages += 1

                if image_area > 0.5 * page_area and text_area < 0.01 * page_area:
                    ocr_like_pages += 1

        if image_pages == total_pages:
            return "scanned"

        if ocr_like_pages > total_pages * 0.5:
            return "scanned+ocr"

        if text_pages > total_pages * 0.8:
            return "digital"

        return "mixed"