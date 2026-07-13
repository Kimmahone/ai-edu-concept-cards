import re
import base64
import glob
import os
from PIL import Image

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Parse all cards
card_regex = re.compile(r'(<article class="card concept-card reveal"([^>]*)>)(.*?)(<\/article>)', re.DOTALL)
cards = []
for match in card_regex.finditer(html):
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

missing_titles = [
    "학생 주도성 (Student Agency)",
    "감정과 학습의 관계",
    "무드미터(Mood Meter)와 RULER",
    "SEL 실천 도구",
    "긍정 훈육의 행동 빙산 모델",
    "드라이커스 — 어긋난 행동 4목표",
    "성장중심·과정중심평가",
    "피드백 유형과 피드백 사다리",
    "등장한 구체 도구들",
    "성찰 도구 — KPT &amp; 체크리스트",
    "수업 속 5대 윤리 쟁점",
    "윤리적 실천 수업 사례",
    "상호코칭 &amp; 피드백 패러다임 전환",
    "성장 설계 (연수 마무리)"
]

# We only have 7 generated images due to quota limits
gen_images = glob.glob('/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/card_gen_*.png')
gen_images.sort()

gen_map = {}
for i, path in enumerate(gen_images):
    if i < len(missing_titles):
        # compress image
        img = Image.open(path)
        img = img.resize((600, 337), Image.LANCZOS)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        import io
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=70)
        b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        gen_map[missing_titles[i]] = f"data:image/jpeg;base64,{b64}"

imgs_obj = {}
new_html = html

for idx, card in enumerate(cards):
    title = card['title']
    inner = card['inner']
    attrs = card['attrs']
    
    img_src = None
    
    # Check if we generated an image for it
    if title in gen_map:
        img_src = gen_map[title]
        # Replace the thumb div
        img_tag = f'<div class="thumb"><img src="{img_src}" alt="{title}"></div>'
        inner = re.sub(r'<div class="thumb">.*?<\/div>', '', inner, flags=re.DOTALL)
        if '<div class="top"' in inner:
            inner = re.sub(r'(<div class="top"[^>]*><\/div>)', r'\1' + img_tag, inner)
        else:
            inner = img_tag + inner
    else:
        # Check if there is an img tag in the thumb
        img_match = re.search(r'<div class="thumb"><img src="([^"]+)"', inner)
        if img_match:
            img_src = img_match.group(1)
        else:
            # Maybe it has an SVG?
            svg_match = re.search(r'<div class="thumb">(<svg.*?</svg>)</div>', inner, re.DOTALL)
            if svg_match:
                svg_content = svg_match.group(1)
                # Encode SVG for data URI
                import urllib.parse
                img_src = "data:image/svg+xml;utf8," + urllib.parse.quote(svg_content)
            else:
                img_src = ""

    # Generate a unique key
    key = f"card_{idx+1}"
    imgs_obj[key] = img_src
    
    # Update data-img in attrs
    if 'data-img="' in attrs:
        attrs = re.sub(r'data-img="[^"]*"', f'data-img="{key}"', attrs)
    else:
        attrs += f' data-img="{key}"'
        
    new_card_str = f'<article class="card concept-card reveal"{attrs}>{inner}</article>'
    new_html = new_html.replace(card['match_str'], new_card_str)

import json
imgs_json = json.dumps(imgs_obj)

# Replace the window.__IMGS object in script
script_replacement = f"window.__IMGS={imgs_json};"
new_html = re.sub(r'window\.__IMGS=\{.*?\};', script_replacement, new_html, flags=re.DOTALL)

with open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated HTML with correct IMGS and new generated images.")
