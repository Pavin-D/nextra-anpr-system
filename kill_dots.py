import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Target the specific wrapper container that holds the header indicator dots
        pattern = r'<div className="relative flex items-center justify-center w-8 h-8">.*?</div>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Removed all header indicator dot containers successfully!")
