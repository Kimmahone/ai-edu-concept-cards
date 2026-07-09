import re
import codecs

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    html = f.read()

def get_color(cat):
    m = re.search(r'data-cat="' + cat + r'" data-color="([^"]+)"', html)
    return m.group(1) if m else "#000000"

def get_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

cards_to_add = [
    {
        "cat": "E",
        "title": "탐구 질문 (Inquiry Question) 설계",
        "def": "<ul><li>단순 사실 확인을 넘어 학생의 호기심을 촉발하고 AI와의 상호작용을 이끌어내는 질문 설계</li><li>백워드 설계의 핵심 질문과 연결되며, 확장된 구성주의에서 'Model B(AI가 학생에게 질문)' 구조를 위한 기반이 됨</li></ul>",
        "insight": "좋은 질문이 좋은 AI 활용을 만든다.",
        "apply": "AI에게 단순히 답을 찾는 것이 아니라, 탐구 질문을 던지며 스스로 지식을 구성하게 하세요.",
        "src": "5과정"
    },
    {
        "cat": "C",
        "title": "DIKW 피라미드와 Verbert 학습 분석 모델",
        "def": "<ul><li><b>DIKW 피라미드</b>: 데이터(Data) → 정보(Info) → 지식(Knowledge) → 지혜(Wisdom)로 승화되는 의미 부여 과정</li><li><b>Verbert 모델</b>: 데이터 수집 → 의미 파악 → 행동(수업 개선)으로 이어지는 학습 분석의 핵심 프레임워크</li></ul>",
        "insight": "데이터는 수집이 아니라 의미 파악과 다음 행동(수업 개선)으로 이어질 때 가치가 있다.",
        "apply": "수집된 학생 데이터를 분석하여 다음 수업의 개선점이나 학생 개인별 맞춤 피드백을 어떻게 줄지 계획해보세요.",
        "src": "4과정"
    },
    {
        "cat": "C",
        "title": "성취도 × 참여도 매트릭스",
        "def": "<ul><li>학생의 학습 데이터를 '성취도'와 '참여도'의 2축으로 나누어 4사분면으로 분류</li><li>자기주도형, 노력형, 흥미상실형, 학습지원필요형 등 각 특성에 맞는 AI·디지털 맞춤형 지원 전략 수립</li></ul>",
        "insight": "성취도와 참여도를 함께 보면 학생이 진짜 필요로 하는 지원이 무엇인지 구체화된다.",
        "apply": "평가 결과(성취도)와 플랫폼 활동 로그(참여도)를 결합하여 학급 학생들을 4사분면에 배치하고 맞춤형 지도를 기획하세요.",
        "src": "4과정, 11과정"
    },
    {
        "cat": "G",
        "title": "진단 결과 3단계 프레임워크",
        "def": "<ul><li>사후 진단 결과를 교육적 성찰로 연결하는 3단계 분석 방법론</li><li>① 사전-사후 비교(변화 찾기) → ② 강점 역량 발견하기 → ③ 성장이 더 필요한 역량과 원인 파악</li></ul>",
        "insight": "진단 결과는 끝이 아니라 시작이다. 강점을 확인하고 부족한 점을 성찰하는 도구다.",
        "apply": "연수 전후의 역량 진단 결과를 비교하고, 성장이 가장 필요한 역량 하나를 골라 다음 학기 실천 목표로 삼으세요.",
        "src": "5과정, 10과정, 13과정"
    }
]

for c in cards_to_add:
    cat = c["cat"]
    color = get_color(cat)
    r, g, b = get_rgb(color)
    
    # We will insert it at the end of the category block
    # Find the last card of this category
    cat_cards = list(re.finditer(r'(<article class="card concept-card reveal"[^>]*data-cat="' + cat + r'".*?</article>)', html, re.DOTALL))
    if cat_cards:
        last_card_match = cat_cards[-1]
        last_card_html = last_card_match.group(1)
        
        # Build new card
        new_card = f"""
      <article class="card concept-card reveal" data-cat="{cat}" data-text="{cat} {c['title']} {re.sub('<[^<]+>', '', c['def'])}" data-color="{color}" data-tag="{cat}-new" data-title="{c['title']}" data-def="{c['def']}" data-insight="{c['insight']}" data-apply="{c['apply']}" data-src="{c['src']}">
        <div class="inner">
          <span class="tag" style="background:rgba({r},{g},{b},0.12);color:{color}">{cat}-new</span>
          <h4>{c['title']}</h4>
          <div class="def">{c['def']}</div>
          <div class="block insight" style="margin-top:18px"><div class="bh" style="color:#9a6a00"><svg viewBox="0 0 24 24" style="width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2V18h6v-1.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z"/></svg>핵심 인사이트</div><p>{c['insight']}</p></div>
          <div class="block apply"><div class="bh" style="color:#0a7d3c"><svg viewBox="0 0 24 24" style="width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>교실에서는</div><p>{c['apply']}</p></div>
          <div class="src" style="margin-top:16px"><svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg><span>{c['src']}</span></div>
          <div class="more" style="color:{color}">자세히 보기 <svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
        </div>
      </article>"""
        
        # Insert after last_card_html
        html = html[:last_card_match.end()] + new_card + html[last_card_match.end():]

# Now re-number tags for C, E, G
for cat in ["C", "E", "G"]:
    cards = re.findall(r'<article class="card concept-card reveal"[^>]*data-cat="' + cat + r'".*?</article>', html, re.DOTALL)
    for i, card_html in enumerate(cards):
        new_card_html = re.sub(r'data-tag="[^"]+"', f'data-tag="{cat}{i+1}"', card_html)
        new_card_html = re.sub(r'<span class="tag"[^>]*>[^<]+</span>', f'<span class="tag" style="background:rgba({get_rgb(get_color(cat))[0]},{get_rgb(get_color(cat))[1]},{get_rgb(get_color(cat))[2]},0.12);color:{get_color(cat)}">{cat}{i+1}</span>', new_card_html)
        html = html.replace(card_html, new_card_html)

# Update total count from 55 to 59
html = html.replace('7개 영역, 55개 개념.', '7개 영역, 59개 개념.')

with codecs.open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'w', 'utf-8') as f:
    f.write(html)

print("Added 4 new cards.")
