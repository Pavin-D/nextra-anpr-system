import re

with open("test.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Removing comments for safer counting
content_no_comments = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)
content_no_strings = re.sub(r'"[^"]*"', '""', content_no_comments)
content_no_strings = re.sub(r"'[^']*'", "''", content_no_strings)
content_no_strings = re.sub(r'`[^`]*`', '``', content_no_strings)

open_divs = len(re.findall(r'<div\b[^>]*>', content_no_strings))
close_divs = len(re.findall(r'</div\s*>', content_no_strings))

print(f"Open <div...>: {open_divs}")
print(f"Close </div>: {close_divs}")
