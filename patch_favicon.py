import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_route = """@app.get("/favicon.ico")
def serve_favicon():
    import os
    if os.path.exists("frontend/public/vite.svg"):
        return FileResponse("frontend/public/vite.svg")
    return {"status": "ok"}

@app.get("/")"""

content = content.replace('@app.get("/")', new_route)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Favicon route added")
