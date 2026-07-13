import fitz
import glob
import unicodedata
import re

def normalize(text):
    text = unicodedata.normalize('NFC', text)
    return re.sub(r'[\s\.\,\·\-\&]+', '', text).lower()

all_pdf_files = glob.glob('교안/*.pdf')
pdf_files = [p for p in all_pdf_files if '설계안' not in unicodedata.normalize('NFC', p)]

terms = [
    "탐구 질문", "DIKW", "Verbert", "성취도", "참여도 매트릭스", "진단 결과", "3단계"
]

for path in pdf_files:
    doc = fitz.open(path)
    for i in range(len(doc)):
        text = normalize(doc[i].get_text("text"))
        for term in terms:
            if normalize(term) in text:
                print(f"Found '{term}' in {path} Page {i}")
