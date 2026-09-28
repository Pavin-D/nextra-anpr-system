import os

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html"]

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. Lock the body to prevent page scrolling (fixes the scrollIntoView bug)
        content = content.replace(
            '<body class="bg-gray-100 text-gray-900 font-sans min-h-screen">', 
            '<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden m-0 p-0">'
        )
        
        # 2. Make root take full height
        content = content.replace(
            '<div id="root"></div>', 
            '<div id="root" class="h-full w-full"></div>'
        )
        
        # 3. Change component h-screen to h-full
        content = content.replace(
            'className="relative w-full h-screen overflow-hidden', 
            'className="relative w-full h-full overflow-hidden'
        )

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Locked document scroll globally to prevent offset bug!")
