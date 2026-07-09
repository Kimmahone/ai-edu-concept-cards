import re
import codecs
import base64

image_paths = {
    '교원 디지털·AI 역량 체계': '/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/teacher_ai_competency_1783587840907.png',
    'GRASPS': '/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/grasps_project_based_1783587863296.png',
    '디지털 큐레이션': '/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/digital_curation_1783587795076.png',
    '데이터 신뢰성과 해석': '/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/data_reliability_analysis_1783587803308.png',
    '협력적 전문성 개발': '/Users/yses/.gemini/antigravity-ide/brain/58870e7c-71a6-4987-bad2-9024f8c3daa8/teacher_collaboration_1783587812585.png'
}

html_file = '인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html'
with codecs.open(html_file, 'r', 'utf-8') as f:
    html = f.read()

for title, path in image_paths.items():
    with open(path, 'rb') as img_f:
        b64 = base64.b64encode(img_f.read()).decode('utf-8')
    
    img_tag = f'<div class="thumb"><img src="data:image/png;base64,{b64}" alt="{title}"></div>'
    
    pattern = re.compile(rf'(<article[^>]*data-title="{title}"[^>]*>.*?)(<div class="thumb">.*?</div>)?(.*?)(</article>)', re.DOTALL)
    
    def repl(m):
        opening = m.group(1)
        opening = re.sub(r'<div class="thumb">.*?</div>', '', opening, flags=re.DOTALL)
        
        rest = m.group(3)
        rest = re.sub(r'<div class="thumb">.*?</div>', '', rest, flags=re.DOTALL)
        
        content = opening + rest
        if '<div class="top"' in content:
            content = re.sub(r'(<div class="top"[^>]*>.*?</div>)', r'\1' + img_tag, content, flags=re.DOTALL)
        else:
            content = opening + img_tag + rest
        return content + m.group(4)
        
    html = pattern.sub(repl, html)

with codecs.open(html_file, 'w', 'utf-8') as f:
    f.write(html)

print("Injected generated images successfully.")
