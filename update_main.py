import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add StaticFiles import if not exists
if "from fastapi.staticfiles import StaticFiles" not in content:
    content = content.replace("from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse", "from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse\nfrom fastapi.staticfiles import StaticFiles")

# Mount assets
if "/assets" not in content:
    content = content.replace("app = FastAPI()", 'app = FastAPI()\n\napp.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")')

# We need to change all `return FileResponse("xxxx.html")` to `return FileResponse("frontend/dist/index.html")`
content = re.sub(r'return FileResponse\("[a-z0-9_]+\.html"\)', 'return FileResponse("frontend/dist/index.html")', content)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Backend updated to serve React SPA!")
