with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()
import re
match = re.search(r'(function Dashboard\(\) \{.*?)class ErrorBoundary', content, re.DOTALL)
if match:
    with open("dashboard_code.txt", "w", encoding="utf-8") as f:
        f.write(match.group(1))
    print("Saved to dashboard_code.txt")
