import fitz
import glob
import re
import base64
import os
import unicodedata

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

card_regex = re.compile(r'(<article class="card concept-card reveal"([^>]*)>)(.*?)(<\/article>)', re.DOTALL)
cards = []
for match in card_regex.finditer(html_content):
    opening, attrs, inner, closing = match.groups()
    title_match = re.search(r'data-title="([^"]*)"', attrs)
    title = title_match.group(1) if title_match else ""
    cards.append({
        'match_str': match.group(0),
        'opening': opening,
        'attrs': attrs,
        'inner': inner,
        'closing': closing,
        'title': title
    })

def normalize(text):
    text = unicodedata.normalize('NFC', text)
    return re.sub(r'[\s\.\,\·\-\&]+', '', text).lower()

all_pdf_files = glob.glob('교안/*.pdf')
pdf_files = [p for p in all_pdf_files if '설계안' not in unicodedata.normalize('NFC', p)]

pdf_data = []
for path in pdf_files:
    doc = fitz.open(path)
    pages = []
    for i in range(len(doc)):
        text = doc[i].get_text("text")
        pages.append({
            'index': i,
            'text': text,
            'norm_text': normalize(text)
        })
    pdf_data.append({'path': path, 'doc': doc, 'pages': pages})

def find_best_page(title):
    norm_title = normalize(title)
    
    if "grasps" in norm_title or "디지털큐레이션" in norm_title:
        return None, None

    # Keyword mapping for hard-to-find concepts
    keywords = []
    if "정량vs정성데이터" in norm_title: keywords = ["정량", "정성"]
    elif "공동주도성" in norm_title: keywords = ["공동주도성"]
    elif "중요해진이유" in norm_title: keywords = ["중요해진"]
    elif "무드미터" in norm_title: keywords = ["무드미터"]
    elif "sel실천도구" in norm_title: keywords = ["sel", "실천도구"]
    elif "빙산" in norm_title: keywords = ["빙산"]
    elif "드라이커스" in norm_title or "어긋난" in norm_title: keywords = ["어긋난", "목표"]
    elif "학생맞춤학습지원기능" in norm_title: keywords = ["학생맞춤", "학습지원"]
    elif "학생참여수업지원기능" in norm_title: keywords = ["학생참여", "수업지원"]
    elif "과정중심평가지원기능" in norm_title: keywords = ["과정중심평가", "지원기능"]
    elif "등장한구체도구들" in norm_title: keywords = ["구체도구"]
    elif "촉진5전략" in norm_title: keywords = ["촉진", "5전략"]
    elif "상호작용원리" in norm_title: keywords = ["상호작용"]
    elif "과정중심평가실행4요소" in norm_title: keywords = ["실행4요소"]
    elif "과정중심평가5국면" in norm_title: keywords = ["5국면"]
    elif "시각화분석도구" in norm_title: keywords = ["시각화", "분석도구"]
    elif "신뢰성과해석" in norm_title: keywords = ["신뢰성", "해석"]
    elif "성찰도구kpt" in norm_title: keywords = ["kpt", "체크리스트"]
    elif "디지털교육규범" in norm_title: keywords = ["규범", "4대기준"]
    elif "학습데이터점검" in norm_title: keywords = ["점검", "4기준"]
    elif "상호코칭피드백" in norm_title: keywords = ["상호코칭", "패러다임"]
    elif "탐구질문" in norm_title: keywords = ["탐구", "질문"]
    elif "dikw" in norm_title: keywords = ["dikw"]
    elif "성취도" in norm_title: keywords = ["성취도", "참여도"]
    elif "진단결과" in norm_title: keywords = ["진단결과", "3단계"]
    elif "ai디지털활용과정중심평가" in norm_title: keywords = ["5국면"]

    
    # 1. exact match
    for pd in pdf_data:
        for p in pd['pages']:
            if p['index'] < 3 or '목차' in p['norm_text'] or '학습목표' in p['norm_text'] or '차례' in p['norm_text']:
                continue
            if norm_title in p['norm_text']:
                return pd['doc'], p['index']

    # 2. keyword match
    if keywords:
        for pd in pdf_data:
            for p in pd['pages']:
                if p['index'] < 3 or '목차' in p['norm_text'] or '학습목표' in p['norm_text'] or '차례' in p['norm_text']:
                    continue
                if all(k in p['norm_text'] for k in keywords):
                    return pd['doc'], p['index']
                    
    # 3. First 6 chars
    if len(norm_title) > 5:
        short_title = norm_title[:6]
        for pd in pdf_data:
            for p in pd['pages']:
                if p['index'] < 3 or '목차' in p['norm_text'] or '학습목표' in p['norm_text'] or '차례' in p['norm_text']:
                    continue
                if short_title in p['norm_text']:
                    return pd['doc'], p['index']

                    
    return None, None

new_html_content = html_content
success_count = 0

for card in cards:
    title = card['title']
    doc, page_idx = find_best_page(title)
    if doc is not None:
        page = doc[page_idx]
        pix = page.get_pixmap(matrix=fitz.Matrix(0.6, 0.6))
        img_bytes = pix.tobytes("jpeg", jpg_quality=65)
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        img_src = f"data:image/jpeg;base64,{b64}"
        
        inner = card['inner']
        img_tag = f'<div class="thumb"><img src="{img_src}" alt="{title}"></div>'
        
        inner = re.sub(r'<div class="thumb">.*?<\/div>', '', inner, flags=re.DOTALL)
        if '<div class="top"' in inner:
            inner = re.sub(r'(<div class="top"[^>]*><\/div>)', r'\1' + img_tag, inner)
        else:
            inner = img_tag + inner
            
        new_card_str = card['opening'] + inner + card['closing']
        new_html_content = new_html_content.replace(card['match_str'], new_card_str)
        success_count += 1
    else:
        print(f"Still missing: {title}")

with open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print(f"Updated {success_count} cards with slide images.")
