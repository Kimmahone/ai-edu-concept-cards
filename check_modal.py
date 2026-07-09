import re
import codecs

with codecs.open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'r', 'utf-8') as f:
    html = f.read()

# Check script part
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    print(script_match.group(1)[:1000])

