import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern for blinking dots before text (usually mr-2 or mr-3)
pattern = r'<(span|div) className="[^"]*rounded-full[^"]*animate-(pulse|ping)[^"]*mr-[0-9][^"]*"></\1>'
matches = re.findall(pattern, content)
print(f"Found {len(matches)} blinking dots in alerts.html")

# Remove them
content = re.sub(pattern, '', content)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)
