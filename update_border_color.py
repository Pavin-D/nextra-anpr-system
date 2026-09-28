import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        old_wrapper = "bg-white/60 border border-gray-200 shadow-sm backdrop-blur-md overflow-hidden p-0"
        new_wrapper = "bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md overflow-hidden p-0"
        
        content = content.replace(old_wrapper, new_wrapper)

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Added indigo-themed fixed border!")
