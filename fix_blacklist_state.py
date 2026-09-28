import re

with open("blacklist.html", "r", encoding="utf-8") as f:
    content = f.read()

# Inject showSidebar state
if "const [showSidebar, setShowSidebar] = React.useState(true);" not in content:
    content = content.replace(
        "const [isSubmitting, setIsSubmitting] = React.useState(false);",
        "const [isSubmitting, setIsSubmitting] = React.useState(false);\n    const [showSidebar, setShowSidebar] = React.useState(true);"
    )
    with open("blacklist.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed blacklist.html showSidebar error!")
else:
    print("State already exists.")
