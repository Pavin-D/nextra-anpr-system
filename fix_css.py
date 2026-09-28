with open("frontend/src/index.css", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("@tailwind base;\n", "")
content = content.replace("@tailwind components;\n", "")
content = content.replace("@tailwind utilities;\n", "")
content = content.replace("@tailwind base;\r\n", "")
content = content.replace("@tailwind components;\r\n", "")
content = content.replace("@tailwind utilities;\r\n", "")

content = '@import "tailwindcss";\n' + content

with open("frontend/src/index.css", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.css to use Tailwind v4 import!")
