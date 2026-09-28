import os

files = ["index.html", "tracking.html", "geofence.html"]

old_anim = "transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}"
new_anim = "transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] origin-left ${showSidebar ? 'translate-x-0 opacity-100 scale-100' : '-translate-x-[50px] opacity-0 scale-95 pointer-events-none'}"

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace(old_anim, new_anim)
            
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

print("Upgraded animations on map pages!")
