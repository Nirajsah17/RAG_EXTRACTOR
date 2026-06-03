from extractor.pdf.extractor import PdfExtractor


class ExtractionRouter:
    def get_extractor(self, pdf_type: str, pdf_path: str):
        normalized_type = pdf_type.lower().strip()

        if normalized_type in {'digital', 'mixed'}:
            from extractor.pdf.pdfplumber_extractor import PdfPlumberExtractor
            from extractor.pdf.pymupdf_extractor import PyMuPDFExtractor

            return PdfExtractor(
                pdf_path,
                [
                    PdfPlumberExtractor(pdf_path),
                    PyMuPDFExtractor(pdf_path),
                ],
            )

        if normalized_type == 'scanned':
            from extractor.pdf.pymupdf_extractor import PyMuPDFExtractor

            return PyMuPDFExtractor(pdf_path)

        if normalized_type == 'scanned+ocr':
            from extractor.pdf.pymupdf_extractor import PyMuPDFExtractor

            return PdfExtractor(
                pdf_path,
                [PyMuPDFExtractor(pdf_path)],
            )

        raise ValueError(f'Unsupported PDF type: {pdf_type}')
