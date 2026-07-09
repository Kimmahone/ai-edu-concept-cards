import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    content = f.read()

articles = re.findall(r'<article[^>]*data-cat="A"[^>]*data-title="([^"]*)"', content)
for i, a in enumerate(articles):
    print(f"{i+1}: {a}")

