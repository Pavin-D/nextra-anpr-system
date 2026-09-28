with open("test.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if i > len(lines) - 30:
        print(f"{i+1}: {line}", end="")
