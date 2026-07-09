import fitz
import glob
import os
import unicodedata

pdfs = glob.glob('교안/*교안*.pdf')
pdfs.sort()

all_titles = []
for pdf in pdfs:
    normalized_path = unicodedata.normalize('NFC', pdf)
    doc = fitz.open(normalized_path)
    print(f"--- {os.path.basename(pdf)} ---")
    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text()
        lines = text.strip().split('\n')
        # Heuristic to get title: top most non-empty text, usually line 0 or 1.
        if len(lines) > 0:
            title = lines[0].strip()
            if len(title) < 3 and len(lines) > 1:
                title = lines[1].strip()
            # print(f"Page {i}: {title}")
