const fs = require('fs');
const html = fs.readFileSync('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'utf8');

const regex = /<article class="card concept-card reveal"([^>]*)>(.*?)<\/article>/g;
let match;
let noThumb = [];

while ((match = regex.exec(html)) !== null) {
  const attrs = match[1];
  const innerHtml = match[2];
  const titleMatch = attrs.match(/data-title="([^"]*)"/);
  const title = titleMatch ? titleMatch[1] : 'Unknown';
  
  if (!innerHtml.includes('<div class="thumb">') && !innerHtml.includes('<img')) {
    noThumb.push(title);
  }
}

console.log(`Cards missing thumb/img: ${noThumb.length}`);
noThumb.forEach(t => console.log('- ' + t));
