import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_routes = """
@app.get("/api/v1/videos")
def list_videos():
    import glob, os, datetime
    files = glob.glob("data/uploads/*.mp4")
    videos = []
    for f in files:
        videos.append({
            "filename": os.path.basename(f),
            "size": f"{os.path.getsize(f) / (1024*1024):.2f} MB",
            "date": datetime.datetime.fromtimestamp(os.path.getmtime(f)).isoformat()
        })
    # sort by date descending
    videos.sort(key=lambda x: x["date"], reverse=True)
    return {"videos": videos}

@app.get("/api/v1/videos/play/{filename}")
def serve_video(filename: str):
    import os
    path = f"data/uploads/{filename}"
    if not os.path.exists(path):
        return {"error": "Not found"}
    return FileResponse(path, media_type="video/mp4")

@app.delete("/api/v1/videos/delete/{filename}")
def delete_video(filename: str):
    import os
    path = f"data/uploads/{filename}"
    if os.path.exists(path):
        os.remove(path)
        return {"success": True}
    return {"error": "Not found"}

@app.get("/api/v1/progress")"""

content = content.replace('@app.get("/api/v1/progress")', new_routes)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Backend patched")
