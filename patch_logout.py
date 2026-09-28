import glob
import re

for filepath in glob.glob("frontend/src/pages/*.jsx"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "onClick={triggerLogout}" in content:
        content = content.replace("onClick={triggerLogout}", "onClick={() => window.triggerLogout()}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("Patched all JSX to use window.triggerLogout")
