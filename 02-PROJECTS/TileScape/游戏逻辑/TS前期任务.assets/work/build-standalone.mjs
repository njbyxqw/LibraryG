import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
let html = fs.readFileSync(path.join(root, 'work/ts-tile-goal-lines-template.html'), 'utf8');
for (const name of ['map-concept', 'star-storyboard', 'rewards-concept', 'rabbit-concept', 'bird-shelter-concept']) {
  const data = fs.readFileSync(path.join(root, `work/${name}.jpg`)).toString('base64');
  html = html.replaceAll(`src="assets/${name}.png"`, `src="data:image/jpeg;base64,${data}"`);
}
fs.writeFileSync(path.join(root, 'outputs/ts-tile-goal-lines.html'), html);
console.log('Standalone HTML:', (Buffer.byteLength(html) / 1024 / 1024).toFixed(2), 'MB');
