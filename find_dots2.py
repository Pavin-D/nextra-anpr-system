import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html"]

pattern = r'<(span|div)\s+className="[^"]*\b(w-[0-4](?:\.[0-9])?|h-[0-4](?:\.[0-9])?)\b[^"]*\brounded-full\b[^"]*"(?:\s*/>|>\s*</\1>)'
# Since order doesn't matter, let's just write a custom script to parse it nicely.

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        full_matches = re.finditer(r'<(span|div)\s+className="([^"]+)"(?:\s*/>|>\s*</\1>)', content)
        if full_matches:
            for m in full_matches:
                classes = m.group(2)
                # Check for rounded-full and a small dimension
                if 'rounded-full' in classes and any(dim in classes for dim in ['w-1', 'w-1.5', 'w-2', 'w-2.5', 'w-3', 'w-3.5', 'w-4', 'h-1', 'h-1.5', 'h-2', 'h-2.5', 'h-3', 'h-3.5', 'h-4']):
                    print(f"{file}: {m.group(0)}")

