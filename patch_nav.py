import os
import re

pages_dir = "frontend/src/pages"
files = [f for f in os.listdir(pages_dir) if f.endswith(".jsx") and f != "Login.jsx"]

nav_links = [
    ("Dashboard", "/", "Dashboard"),
    ("Tracking", "/tracking", "Tracking"),
    ("Blacklist", "/blacklist", "Blacklist"),
    ("Geofence", "/geofence", "Geofence"),
    ("Chat", "/chat", "AI Chat"),
    ("Alerts", "/alerts", "Alerts"),
    ("Database", "/database", "Database"),
    ("Videos", "/videos", "Videos")
]

logout_btn = '<button onClick={() => window.triggerLogout()} className="px-4 py-2 ml-2 flex items-center text-xs font-black uppercase tracking-wider rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>'

# Regex to capture the nav div: starts with <div className="hidden md:flex space-x-2"> and ends with the closing </div> of that block
regex = re.compile(r'<div className="hidden md:flex space-x-2">.*?</button>\s*</div>', re.DOTALL)

for filename in files:
    filepath = os.path.join(pages_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    page_name = filename.replace(".jsx", "")
    
    new_nav = '<div className="hidden md:flex space-x-2">\n'
    
    for name, url, label in nav_links:
        # Determine if this is the active page
        is_active = (name == page_name)
        
        if is_active:
            if name == "Alerts":
                css = 'px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-rose-500 to-red-500 text-white shadow-lg shadow-rose-500/30 transition-transform transform hover:-translate-y-0.5'
            else:
                css = 'px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5'
        else:
            if name == "Alerts":
                css = 'px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors'
            else:
                css = 'px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors'
                
        new_nav += f'                    <a href="{url}" className="{css}">{label}</a>\n'
        
    new_nav += f'                    {logout_btn}\n                </div>'
    
    # Replace it in the file
    new_content = regex.sub(new_nav, content)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated Navigation in {filename}")

print("Navigation sync complete.")
