import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_route = """@app.get("/videos")
def serve_videos():
    return FileResponse("frontend/dist/index.html")

@app.get("/database")"""

content = content.replace('@app.get("/database")', new_route)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Added /videos frontend route to FastAPI")
