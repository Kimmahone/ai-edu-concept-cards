import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    content = f.read()

# 1. Find all data-title
titles = re.findall(r'data-title="([^"]*)"', content)
print(f"Total titles: {len(titles)}")
for i, t in enumerate(titles):
    print(f"{i+1}: {t}")

