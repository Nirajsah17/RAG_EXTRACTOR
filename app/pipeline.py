from extractor.classifier import FileClassifier
from extractor.native_pdf_extractor import NativePdfExtractor
from utils.constant import DocumentType
class ExtractionPipeline:
  def __init__(self, input_path, output_path):
    self.input_path = input_path
    self.output_path = output_path
    self.classifier = FileClassifier()
    self.extractor = NativePdfExtractor(self.output_path)
    
  def run(self):
    classified = self.classifier.classify(self.input_path)
    doc_label = classified.get("document_label")
    if DocumentType.SCANNED_PDF_DOCUMENT == doc_label:
      print("Not supporting, terminating the process .......\n")
    self.extractor.extract(self.input_path)
    print(doc_label)