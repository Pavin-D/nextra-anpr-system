import glob
import re

# 1. Remove LIVE ALERTS from index.html
try:
    with open("index.html", "r", encoding="utf-8") as f:
        idx_content = f.read()
    
    # We will remove the block starting from {/* LIVE ALERTS */} up to the next {/* TELEMETRY */}
    pattern = re.compile(r'\{/\*\s*LIVE ALERTS\s*\*/\}.*?(?=\{/\*\s*TELEMETRY\s*\*/\})', re.DOTALL)
    idx_content = pattern.sub('', idx_content)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(idx_content)
    print("Removed Live Alerts block from index.html")
except Exception as e:
    print(f"Error modifying index.html: {e}")

# 2. Add /alerts to all html navbars
new_link_dark = '\n                            <a href="/alerts" className="px-4 py-1.5 text-sm font-bold rounded-md text-slate-400 hover:text-white hover:bg-slate-950">Threat Alerts</a>'
new_link_light = '\n                            <a href="/alerts" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Threat Alerts</a>'

for file in glob.glob("*.html"):
    if file == "alerts.html":
        continue
    
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # For index.html (which is in white theme now)
        content = content.replace('AI Chat Search</a>\n                        </div>', 'AI Chat Search</a>' + new_link_light + '\n                        </div>')
        # For other pages (which might be dark theme or white theme, wait, earlier the user reverted all to dark theme, but then only changed index.html to white theme).
        # So other pages are still dark theme!
        content = content.replace('AI Chat Search</a>\r\n                        </div>', 'AI Chat Search</a>' + new_link_dark + '\r\n                        </div>')
        
        # Safe catch-all replace
        if '<a href="/alerts"' not in content:
            # Let's do regex to find AI Chat Search anchor and append
            content = re.sub(r'(<a href="/chat"[^>]*>AI Chat Search</a>)', r'\1' + new_link_dark, content)
            
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error modifying {file}: {e}")

print("Added Alerts link to all navbars.")
