with open("alerts.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "return (" in line:
        start = i
        break
print("".join(lines[start:]))
