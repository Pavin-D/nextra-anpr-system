import re
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("extends React.Component {", "class ErrorBoundary extends React.Component {")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Restored 'class ErrorBoundary'")
