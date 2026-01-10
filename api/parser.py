import fitz
from pathlib import Path

#Converts pdf to a string
def convert_pdf_to_string(pdf_file):
    if pdf_file.exists():
        with open(pdf_file, "rb") as f:
            content = _extract_text_from_pdf(f.read())
            return content
    else:
        print(f"File not found at {pdf_file}")

def _extract_text_from_pdf(file_bytes: bytes) -> str:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        print("pdf extracted")
        return "\n".join(page.get_text() for page in doc)
    

# Finds the file
# DATA_DIR = Path(__file__).parent / "data"
# pdf_file = DATA_DIR / "testresume.pdf"
# open_pdf(pdf_file)