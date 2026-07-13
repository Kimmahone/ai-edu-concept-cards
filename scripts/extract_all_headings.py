import fitz
import os
import unicodedata

pdf_dir = '교안'
pdfs = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
pdfs.sort()

with open('headings_dump.md', 'w') as f:
    for pdf in pdfs:
        # only want the main slide files, skip 수업 설계안 for now
        if '설계안' in pdf or '설계안' in pdf:
            continue
        normalized_path = unicodedata.normalize('NFC', pdf)
        doc = fitz.open(normalized_path)
        f.write(f"\n## {os.path.basename(pdf)}\n")
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if len(lines) > 0:
                title = lines[0]
                if len(title) < 5 and len(lines) > 1:
                    title = lines[1]
                f.write(f"- Page {i+1}: {title}\n")
