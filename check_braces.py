import re
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# count braces in the babel script
script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if script_match:
    script = script_match.group(1)
    script = re.sub(r'//.*', '', script)
    script = re.sub(r'/\*.*?\*/', '', script, flags=re.DOTALL)
    script = re.sub(r'\{/\*.*?\*/\}', '', script, flags=re.DOTALL)
    print(f"{{: {script.count('{')}")
    print(f"}}: {script.count('}')}")
