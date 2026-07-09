import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    html = f.read()

# 1. Update "과정 중심 평가 5국면" to "AI 디지털 활용 과정중심평가"
html = re.sub(
    r'data-title="과정 중심 평가 5국면"',
    r'data-title="AI 디지털 활용 과정중심평가"',
    html
)
html = re.sub(
    r'<h4>과정 중심 평가 5국면</h4>',
    r'<h4>AI 디지털 활용 과정중심평가</h4>',
    html
)
html = re.sub(
    r'<div class="def"><b>진단 · 학습 · 평가 · 피드백 · 성찰</b> — 교사\(T\)/학생\(S\) 활동에 AI·디지털 기능을 색상으로 구분 배치합니다. 도구를 쓰지 않는 국면을 비워두는 것도 교사의 <b>의도적 선택</b>.</div>',
    r'<div class="def"><b>진단 · 학습 · 평가 · 피드백 · 성찰</b> — 과정중심평가의 흐름을 수업 설계안에 담아내고, 교사(T)/학생(S) 활동에 트라이디스, AI튜터 등 AI·디지털 기능을 색상으로 구분 배치하여 과정중심평가를 가시화하는 기법</div>',
    html
)

# 2. Move data concepts to Category C
# The data concepts are currently in Category F (F1, F2, F3)
# We will change their data-cat to "C" and data-tag to C10, C11, C12
# C color is #ff9500 (orange-ish). Let's check what color C uses.
c_color = "#ff9500" # I will use this. Wait, let me check C color in html.
c_color_match = re.search(r'data-cat="C" data-color="([^"]+)"', html)
if c_color_match:
    c_color = c_color_match.group(1)

for title in ["학습 데이터의 종류", "데이터 시각화·분석 도구", "데이터 신뢰성과 해석"]:
    # Find the article
    card_regex = re.compile(r'(<article class="card concept-card reveal"[^>]*data-title="' + title + r'".*?</article>)', re.DOTALL)
    card_match = card_regex.search(html)
    if card_match:
        card_html = card_match.group(1)
        # Update data-cat
        card_html = re.sub(r'data-cat="F"', 'data-cat="C"', card_html)
        # Update data-color
        card_html = re.sub(r'data-color="[^"]+"', f'data-color="{c_color}"', card_html)
        # Update data-tag from F1, F2, F3 to C...
        card_html = re.sub(r'data-tag="F\d+"', 'data-tag="C-new"', card_html)
        # Update inline tag background color
        card_html = re.sub(r'background:rgba\([^)]+\);color:#[0-9a-fA-F]+', f'background:rgba(255,149,0,0.12);color:{c_color}', card_html)
        card_html = re.sub(r'>F\d+<', '>C-new<', card_html)
        # Replace in html
        html = html.replace(card_match.group(1), card_html)

# Now re-number all C tags
c_cards = re.findall(r'<article class="card concept-card reveal"[^>]*data-cat="C".*?</article>', html, re.DOTALL)
for i, card_html in enumerate(c_cards):
    new_card_html = re.sub(r'data-tag="[^"]+"', f'data-tag="C{i+1}"', card_html)
    new_card_html = re.sub(r'<span class="tag"([^>]*)>[^<]+</span>', rf'<span class="tag"\1>C{i+1}</span>', new_card_html)
    html = html.replace(card_html, new_card_html)

# Re-number F tags
f_cards = re.findall(r'<article class="card concept-card reveal"[^>]*data-cat="F".*?</article>', html, re.DOTALL)
for i, card_html in enumerate(f_cards):
    new_card_html = re.sub(r'data-tag="[^"]+"', f'data-tag="F{i+1}"', card_html)
    new_card_html = re.sub(r'<span class="tag"([^>]*)>[^<]+</span>', rf'<span class="tag"\1>F{i+1}</span>', new_card_html)
    html = html.replace(card_html, new_card_html)


with codecs.open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'w', 'utf-8') as f:
    f.write(html)

print("Updated HTML with rename and category movements.")
