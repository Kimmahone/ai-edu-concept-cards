import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    content = f.read()

match = re.search(r'<article class="card concept-card reveal"[^>]*data-title="학습 데이터의 종류".*?</article>', content, re.DOTALL)
if match:
    print(match.group(0)[:500])
