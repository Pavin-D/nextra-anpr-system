import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix layout wrapper
content = content.replace(
    '<div className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-row">',
    '<div className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col">'
)

content = content.replace(
    '{/* TABLE SECTION */}',
    '<div className="flex flex-row flex-1 overflow-hidden">\n                        {/* TABLE SECTION */}'
)

content = content.replace(
    '                            </div>\n                        )}',
    '                            </div>\n                        )}\n                        </div>'
)

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed layout wrappers")
