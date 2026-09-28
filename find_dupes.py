with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "function Dashboard()" in line:
        print(f"Line {i}: {line.strip()}")
