import re

with open("test.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content_no_comments = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)

tags = ["svg", "path", "span", "a", "button", "table", "thead", "tr", "th", "tbody", "td", "h1", "h2", "h3", "p", "div"]
for tag in tags:
    opens = len(re.findall(rf'<{tag}\b[^>]*>', content_no_comments))
    closes = len(re.findall(rf'</{tag}\s*>', content_no_comments))
    if opens != closes:
        print(f"Mismatch in {tag}: {opens} open vs {closes} close")
