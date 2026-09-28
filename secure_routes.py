import os

files = ["index.html", "tracking.html", "blacklist.html", "geofence.html", "chat.html", "alerts.html", "database.html"]

auth_guard = """        // --- SECURE ROUTING ---
        if (!localStorage.getItem('nextra_token')) {
            window.location.href = '/login';
        }
"""

for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "SECURE ROUTING" not in content:
            # Insert right after <script type="text/babel">
            content = content.replace('<script type="text/babel">', '<script type="text/babel">\n' + auth_guard)
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

print("Applied frontend routing security to all pages!")
