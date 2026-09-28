with open("tracking.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('setStatus("Error loading trajectory network.");', 'setStatus("");')

with open("tracking.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed error text")
