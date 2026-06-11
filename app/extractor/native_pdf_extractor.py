import pymupdf4llm
from pathlib import Path

from utils.util import file_to_timestamp_file
class NativePdfExtractor():
  def __init__(self, output_path):
    self.output_path = output_path
  
  def extract(self, pdf_path:str):
    try:
      name = file_to_timestamp_file(pdf_path)
      markdown_text = pymupdf4llm.to_markdown(pdf_path)
      output_name = f"{self.output_path}/{name}.md"
      print(f"Output name : {output_name}")
      file_path = Path(output_name)
      file_path.parent.mkdir(parents=True, exist_ok=True)
      with open (file_path, "w", encoding="utf-8") as file:
        file.write(markdown_text)
    except Exception :
      print("Failed to extract the pdf file", Exception)

    