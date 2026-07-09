const fs = require('fs');
const html = fs.readFileSync('인공지능활용_선도교사연수_초등_핵심개념_웹사이트.html', 'utf8');

const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (scriptMatch) {
    const script = scriptMatch[1];
    const lines = script.split('\n');
    lines.forEach((line, idx) => {
        if (line.includes('modal') || line.includes('IMGS') || line.includes('data-img')) {
            console.log(`L${idx+1}: ${line}`);
        }
    });
} else {
    console.log("No script tag found.");
}
