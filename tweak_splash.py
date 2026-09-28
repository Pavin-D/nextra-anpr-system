import re

with open("login.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the specific text "Biometric Lock Engaged"
content = re.sub(
    r'<p className="[^"]*">Biometric Lock Engaged</p>',
    '',
    content
)

# Change the gradient color of the splash screen
# Old: bg-gradient-to-br from-indigo-600 via-fuchsia-600 to-cyan-500
# New: bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 (Deep, sleek command center dark theme)
content = content.replace(
    "bg-gradient-to-br from-indigo-600 via-fuchsia-600 to-cyan-500",
    "bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900"
)

with open("login.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated background gradient and removed text!")
