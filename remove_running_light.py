import os
import re

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the colorful wrapper on the main containers with a clean, solid glassmorphism wrapper
        # We target the specific gradient strings used for the wrappers (not the body background or the navbar)
        pattern1 = r'bg-gradient-to-br from-fuchsia-500 via-cyan-400 to-indigo-500 p-\[2px\] shadow-\[.*?\]'
        replacement = 'bg-white/60 border border-gray-200 shadow-sm backdrop-blur-md overflow-hidden p-0'
        content = re.sub(pattern1, replacement, content)
        
        pattern2 = r'bg-gradient-to-br from-indigo-500 via-cyan-400 to-fuchsia-500 p-\[2px\] shadow-\[.*?\]'
        content = re.sub(pattern2, replacement, content)

        # Ensure inner panels that had rounded-[22px] now have rounded-none or rounded-3xl so they don't double-round inside the p-0 wrapper
        # The parent is rounded-3xl. If child is rounded-[22px] with p-0, there will be tiny gaps in the corners.
        # We can just change 'rounded-[22px]' to 'rounded-none' for the inner wrappers since the parent has overflow-hidden now.
        content = content.replace('rounded-[22px]', 'rounded-none')

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Removed running light gradient from content containers!")
