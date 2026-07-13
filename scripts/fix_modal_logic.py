import re
import codecs

with codecs.open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace the modal logic in the script
# Old:
#  var img=d.img?'<div class="mimg"><img src="'+IMGS[d.img]+'" alt=""></div>':'';
# New:
#  var thumb = c.querySelector('.thumb img');
#  var imgSrc = thumb ? thumb.src : (d.img ? IMGS[d.img] : '');
#  var img = imgSrc ? '<div class="mimg"><img src="'+imgSrc+'" alt=""></div>' : '';

old_script = "var img=d.img?'<div class=\"mimg\"><img src=\"'+IMGS[d.img]+'\" alt=\"\"></div>':'';"
new_script = "var thumb = c.querySelector('.thumb img'); var imgSrc = thumb ? thumb.src : (d.img ? IMGS[d.img] : ''); var img = imgSrc ? '<div class=\"mimg\"><img src=\"'+imgSrc+'\" alt=\"\"></div>' : '';"

html = html.replace(old_script, new_script)

with codecs.open('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'w', 'utf-8') as f:
    f.write(html)

print("Fixed modal logic.")
