import pdfplumber
from unicodedata import normalize

with pdfplumber.open("input/japanese_sample.pdf") as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        norm_text = normalize("NFKC", text) if text else ""
        print(f"\n--- Page {i} ---\n{norm_text[:500]}")