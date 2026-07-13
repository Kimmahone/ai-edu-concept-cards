import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    content = f.read()

filters = re.findall(r'<button class="filter-btn" data-cat="([A-G])">(.*?)</button>', content)
for f in filters:
    print(f[0] + ": " + f[1])

