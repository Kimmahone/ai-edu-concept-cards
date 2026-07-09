import fitz
import glob
import unicodedata
import re
import os

def normalize(text):
    text = unicodedata.normalize('NFC', text)
    # Remove all spaces and non-word chars
    return re.sub(r'[\s\.\,\·\-\&\?\!\(\)\[\]]+', '', text).lower()

pdf_files = glob.glob('교안/*.pdf')
pdf_files = [p for p in pdf_files if '설계안' not in unicodedata.normalize('NFC', p)]
pdf_files.sort()

search_queries = {
    "학습 데이터의 정의": ["의도적", "흔적"],
    "정량 vs 정성 데이터": ["정량", "정성"],
    "싱가포르 SLS": ["sls"],
    "교사 역할의 확장": ["역할", "확장"],
    "확장된 구성주의": ["구성주의", "model"],
    "TPACK": ["tpack"],
    "학생 주도성": ["agency"],
    "무드미터": ["무드미터"],
    "긍정 훈육": ["빙산"],
    "드라이커스": ["드라이커스"],
    "백워드": ["백워드"],
    "GRASPS": ["grasps"],
    "WHERETO": ["whereto"],
    "피드백 유형과 피드백 사다리": ["피드백", "사다리"],
    "KERIS 수업설계안": ["keris"],
    "디지털 큐레이션": ["큐레이션"],
    "학생 참여 촉진 5전략": ["5전략"],
    "상호작용 원리": ["상호작용"],
    "과정중심평가 실행 4요소": ["4요소"],
    "과정중심평가 5국면": ["5국면"],
    "KPT & 체크리스트": ["kpt"],
    "5대 윤리 쟁점": ["윤리", "쟁점"],
    "디지털 교육 규범": ["규범"],
    "학습데이터 점검": ["점검"],
    "GROW": ["grow"],
    "상호코칭": ["상호코칭"],
    "성장 설계": ["성장", "로드맵"]
}

for concept, keywords in search_queries.items():
    print(f"\nConcept: {concept} (keywords: {keywords})")
    found = False
    for path in pdf_files:
        doc = fitz.open(path)
        for i in range(len(doc)):
            text = doc[i].get_text("text")
            norm = normalize(text)
            if all(normalize(kw) in norm for kw in keywords):
                filename = os.path.basename(path)
                print(f"  FOUND in {filename} Page {i+1}")
                # print first few lines of page
                snippet = " / ".join([line.strip() for line in text.split("\n") if line.strip()][:3])
                print(f"    Snippet: {snippet}")
                found = True
                break # only first page per PDF is fine
