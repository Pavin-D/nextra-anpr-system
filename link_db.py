import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html"]

link_html = '\n                        <a href="/database" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>'

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # For alerts.html, the Alerts link is active (has text-white, etc)
        # So we match the end of the Alerts link and insert the Database link
        # Find the line containing href="/alerts"
        if 'href="/database"' not in content:
            content = re.sub(
                r'(<a href="/alerts"[^>]*>Alerts</a>)',
                r'\1' + link_html,
                content
            )
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

print("Linked Database page to all navbars!")
