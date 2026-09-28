import os

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

route = """@app.get("/database")
def serve_database():
    return FileResponse("database.html")

"""

if "@app.get(\"/database\")" not in content:
    content = content.replace("@app.get(\"/alerts\")", route + "@app.get(\"/alerts\")")
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Added /database route to main.py")
else:
    print("Route already exists")
