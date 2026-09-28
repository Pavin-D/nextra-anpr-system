import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. Remove all blinking dots (rounded-full + animate-pulse/ping)
        pattern_dots = r'<(span|div)\s+className="[^"]*rounded-full[^"]*animate-(pulse|ping)[^"]*">\s*</\1>'
        content = re.sub(pattern_dots, '', content)
        
        # 2. Fix the alerts border
        # The user requested to use the "same indigo for border of alerts page"
        # Earlier we changed it to: border-2 border-rose-200/80 shadow-[0_0_20px_rgba(244,63,94,0.15)]
        # We need to change it back to the indigo one: border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)]
        if file == "alerts.html":
            content = content.replace("border-rose-200/80 shadow-[0_0_20px_rgba(244,63,94,0.15)]", "border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)]")

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Removed all blinking dots and reverted alerts border to Indigo!")
