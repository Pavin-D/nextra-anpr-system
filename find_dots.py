import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html"]

pattern = r'<(span|div)\s+className="[^"]*\bw-[0-9.]+\s+h-[0-9.]+\b[^"]*\brounded-full\b[^"]*"(?:\s*/>|>\s*</\1>)'

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(pattern, content)
            full_matches = re.finditer(pattern, content)
            if full_matches:
                print(f"--- {file} ---")
                for m in full_matches:
                    print(m.group(0))

