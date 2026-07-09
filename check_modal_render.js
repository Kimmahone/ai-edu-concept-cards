const fs = require('fs');
const html = fs.readFileSync('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'utf8');

const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (scriptMatch) {
    const script = scriptMatch[1];
    const lines = script.split('\n');
    lines.forEach((line, idx) => {
        if (line.includes('mc.innerHTML')) {
            console.log(`L${idx+1}: ${line}`);
            // Also print 3 lines before and after
            for(let i=Math.max(0, idx-2); i<Math.min(lines.length, idx+3); i++) {
                if (i !== idx) console.log(`L${i+1}: ${lines[i]}`);
            }
        }
    });
}
