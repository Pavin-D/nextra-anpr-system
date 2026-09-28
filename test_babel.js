const fs = require('fs');
const babel = require('@babel/standalone');

const content = fs.readFileSync('alerts.html', 'utf8');
const scriptMatch = content.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
if (scriptMatch) {
    try {
        babel.transform(scriptMatch[1], { presets: ['react'] });
        console.log("Compiled successfully!");
    } catch (e) {
        console.error(e.message);
    }
}
