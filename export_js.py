with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if script_match:
    with open("check.js", "w", encoding="utf-8") as f:
        f.write(script_match.group(1))
