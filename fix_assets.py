import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix imports
if "from fastapi.staticfiles import StaticFiles" not in content:
    content = content.replace("from fastapi.responses import FileResponse", "from fastapi.responses import FileResponse\nfrom fastapi.staticfiles import StaticFiles")

# Fix mount
if 'app.mount("/assets"' not in content:
    content = content.replace('app = FastAPI(title="City-Wide ANPR Platform")', 'app = FastAPI(title="City-Wide ANPR Platform")\n\napp.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")')

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected static file mounting for /assets!")
