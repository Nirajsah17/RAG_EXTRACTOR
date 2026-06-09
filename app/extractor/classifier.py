import pymupdf
from collections import Counter


class FileClassifier:
  def __init__(self):
    pass

  def _get_page_features(self, page):
    text_dict = page.get_text("dict")

    word_count = 0
    text_block_count = 0
    font_count = set()

    for block in text_dict.get("blocks", []):
      if block.get("type") == 0:
        text_block_count += 1

        for line in block.get("lines", []):
          for span in line.get("spans", []):
            text = span.get("text", "")
            word_count += len(text.split())

            font = span.get("font")
            if font:
              font_count.add(font)

    return {
      "word_count": word_count,
      "text_block_count": text_block_count,
      "font_count": len(font_count)
    }

  def _classify_page(self, features):
    word_count = features["word_count"]
    text_blocks = features["text_block_count"]

    if word_count >= 50 or text_blocks >= 2:
      return "NATIVE_PDF"
    
    return "SCANNED_PDF"

  def classify(self, pdf_path):
    with pymupdf.open(pdf_path) as doc:
      page_results = []

      for i in range(len(doc)):
        page = doc[i]

        features = self._get_page_features(page)
        label = self._classify_page(features)

        page_results.append({
          "page": i + 1,
          "label": label,
          "features": features
        })

    counts = Counter(p["label"] for p in page_results)
    total = len(page_results)

    native_pct = counts["NATIVE_PDF"] / total

    document_label = (
      "NATIVE_PDF_DOCUMENT"
      if native_pct >= 0.8
      else "SCANNED_PDF_DOCUMENT"
    )

    return {
      "document_label": document_label,
      "page_counts": dict(counts),
      "pages": page_results
    }