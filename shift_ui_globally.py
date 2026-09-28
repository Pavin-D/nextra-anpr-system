import os

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # We need to be careful with the exact replacements
        # Navbar is absolute top-6
        # Main content is absolute top-28
        
        # Replace top-6 with top-10 for the navbar across all files
        content = content.replace('absolute top-6 left-6 right-6', 'absolute top-10 left-6 right-6')
        
        # Replace top-28 with top-32 for the main content across all files
        content = content.replace('absolute top-28', 'absolute top-32')
        
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Shifted the entire UI down safely across all pages!")
