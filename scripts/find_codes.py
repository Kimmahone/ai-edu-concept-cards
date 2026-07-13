import re
with open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'r', encoding='utf-8') as f:
    html = f.read()

for match in re.finditer(r'([^\n]*\b[A-G][1-3]\b[^\n]*)', html):
    line = match.group(1).strip()
    if 'concept-card' in line or 'card' in line or 'def' in line or 'data-' in line:
        print(line[:120])
