import fitz
import glob
import unicodedata
import re

def normalize(text):
    text = unicodedata.normalize('NFC', text)
    return re.sub(r'[\s\.\,\·\-\&]+', '', text).lower()

pdf_files = glob.glob('교안/*.pdf')
pdf_files = [p for p in pdf_files if '설계안' not in unicodedata.normalize('NFC', p)]
pdf_files.sort()

# Let's search for some keys
search_queries = {
    "학습 데이터의 정의": ["의도적 흔적", "비의도적 흔적"],
    "정량 vs 정성 데이터": ["정량", "정성", "William Bruce Cameron"],
    "싱가포르 SLS": ["SLS", "Pedagogical", "Scaffold"],
    "교사 역할의 확장": ["역할의 확장", "대체가 아닌"],
    "확장된 구성주의": ["확장된 구성주의", "Model A"],
    "TPACK": ["TPACK", "AI-TPACK"],
    "학생 주도성": ["Student Agency", "자기 삶과 학습", "주도성"],
    "무드미터": ["무드미터", "Mood Meter", "RULER"],
    "긍정 훈육": ["빙산", "긍정의 훈육"],
    "드라이커스": ["드라이커스", "어긋난 행동"],
    "백워드": ["백워드", "Backward"],
    "GRASPS": ["GRASPS"],
    "WHERETO": ["WHERETO"],
    "피드백 유형과 피드백 사다리": ["피드백 사다리"],
    "KERIS 수업설계안": ["KERIS", "설계안 양식"],
    "디지털 큐레이션": ["큐레이션"],
    "학생 참여 촉진 5전략": ["5전략", "Chi"],
    "상호작용 원리": ["상호작용 원리", "대화 루프"],
    "과정중심평가 실행 4요소": ["실행 4요소", "평가 모먼트"],
    "과정중심평가 5국면": ["5국면"],
    "KPT & 체크리스트": ["KPT", "성찰 체크리스트"],
    "5대 윤리 쟁점": ["5대 윤리 쟁점"],
    "디지털 교육 규범": ["규범 4대 기준"],
    "학습데이터 점검": ["데이터 점검 4기준"],
    "GROW": ["GROW", "Goal"],
    "상호코칭": ["상호코칭"],
    "성장 설계": ["사후 진단", "로드맵"]
}

for concept, keywords in search_queries.items():
    print(f"\nSearching for concept: {concept} (keywords: {keywords})")
    found = False
    for path in pdf_files:
        doc = fitz.open(path)
        for i in range(len(doc)):
            text = doc[i].get_text("text")
            norm = normalize(text)
            if all(normalize(kw) in norm for kw in keywords):
                filename = os.path.basename(path)
                print(f"  FOUND in {filename} Page {i+1}")
                # print a snippet
                snippet = " / ".join([line.strip() for line in text.split("\n") if line.strip()][:5])
                print(f"    Snippet: {snippet}")
                found = True
    if not found:
        print("  NOT FOUND WITH ALL KEYWORDS")
