const fs = require('fs');

let html = fs.readFileSync('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'utf8');

// 1. Remove the <header class="hero"> block completely
html = html.replace(/<header class="hero">[\s\S]*?<\/header>/, '');

// 2. Add images to cards missing images
const icons = {
  'A': 'M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z', 
  'B': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z', 
  'C': 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z', 
  'D': 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z', 
  'E': 'M3 17.25V21h3.75L17.81 10.47l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z', 
  'F': 'M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.5 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z', 
  'G': 'M8 5v14l11-7z', 
  'H': 'M3 3v18h18V3H3zm6 14H7v-5h2v5zm4 0h-2v-3h2v3zm0-5h-2v-2h2v2zm4 5h-2V7h2v10z', 
  'I': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z', 
  'J': 'M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z'
};

const cardRegex = /(<article class="card concept-card reveal"([^>]*)>)(.*?)<\/article>/g;

html = html.replace(cardRegex, (match, openingTag, attrs, innerHtml) => {
  if (innerHtml.includes('<div class="thumb">') || innerHtml.includes('<img')) {
    return match; // Already has image
  }

  const catMatch = attrs.match(/data-cat="([^"]*)"/);
  const colorMatch = attrs.match(/data-color="([^"]*)"/);
  const titleMatch = attrs.match(/data-title="([^"]*)"/);
  
  const cat = catMatch ? catMatch[1] : 'A';
  const color = colorMatch ? colorMatch[1] : '#0071e3';
  const title = titleMatch ? titleMatch[1] : '';
  
  const iconPath = icons[cat] || icons['A'];

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${color}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="${color}" stop-opacity="0.05"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <circle cx="200" cy="100" r="50" fill="${color}" opacity="0.1"/>
  <g transform="translate(160, 60) scale(3.33)">
    <path d="${iconPath}" fill="${color}" opacity="0.8"/>
  </g>
</svg>`;

  const base64 = 'data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64');
  
  const imgTag = `<div class="thumb"><img src="${base64}" alt="${title}"></div>`;
  
  let newInner = innerHtml;
  if (newInner.includes('</div>')) {
    newInner = newInner.replace(/(<div class="top"[^>]*><\/div>)/, '$1' + imgTag);
  } else {
    newInner = imgTag + newInner;
  }
  
  return `${openingTag}${newInner}</article>`;
});

// 3. Add copyright and author to footer
const footerNotice = `\n  <div class="note">© 2026 인공지능 활용 선도교사 연수. 저작자: 포항양덕초 교사 김정준</div>\n</div></footer>`;
html = html.replace(/<\/div><\/footer>/, footerNotice);

fs.writeFileSync('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', html, 'utf8');
console.log('Update complete!');
