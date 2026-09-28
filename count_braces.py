with open("test.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re
content = re.sub(r'//.*', '', content)
content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
content = re.sub(r'\{/\*.*?\*/\}', '', content, flags=re.DOTALL)

opens = content.count('{')
closes = content.count('}')
print(f"{{: {opens}, }}: {closes}")

opens_p = content.count('(')
closes_p = content.count(')')
print(f"(: {opens_p}, ): {closes_p}")
