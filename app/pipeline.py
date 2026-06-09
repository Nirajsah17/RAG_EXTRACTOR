from extractor.classifier import FileClassifier
class ExtractionPipeline:
  def __init__(self, input_path, use_layout_aware=False):
    self.input_path = input_path
    self.use_layout_aware = use_layout_aware
    self.classifier = FileClassifier()
    
  def run(self):
    classified = self.classifier.classify(self.input_path)
    print(classified)
    return classified