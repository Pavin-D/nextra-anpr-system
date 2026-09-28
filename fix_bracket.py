with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("} catch(e) { console.error(e); };", "} catch(e) { console.error(e); }\n                };")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed fetchTelemetry closing bracket")
