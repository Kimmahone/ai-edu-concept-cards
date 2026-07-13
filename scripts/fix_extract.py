import codecs
import re

with codecs.open('extract_slides.py', 'r', 'utf-8') as f:
    content = f.read()

# I want to add a check inside find_best_page to skip bad pages.
# Let's find the loops.
replacement = """    # 1. exact match
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
"""

# The original has:
#    # 1. exact match
#    for pd in pdf_data:
# ...
#    # 3. First 6 chars
# ...
#                    return pd['doc'], p['index']

content = re.sub(r'    # 1\. exact match.*return pd\[\'doc\'\], p\[\'index\'\]', replacement, content, flags=re.DOTALL)

# Add explicit skip for grasps and 디지털 큐레이션 so they return None and we can use generated images.
skip_logic = """
    if "grasps" in norm_title or "디지털큐레이션" in norm_title:
        return None, None
"""
content = content.replace("def find_best_page(title):", "def find_best_page(title):" + skip_logic)

with codecs.open('extract_slides.py', 'w', 'utf-8') as f:
    f.write(content)

print("Updated extract_slides.py")
