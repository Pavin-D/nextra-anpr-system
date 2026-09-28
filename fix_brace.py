import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '                </div>\n            );\n\n        const root',
    '                </div>\n            );\n        }\n\n        const root'
)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Added missing closing brace to AlertsApp")
