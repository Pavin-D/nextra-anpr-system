import re

with open("alerts.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if script_match:
    with open("test.jsx", "w", encoding="utf-8") as f:
        f.write(script_match.group(1))
    print("Extracted test.jsx")
