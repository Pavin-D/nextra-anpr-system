import os

for filename in os.listdir("."):
    if filename.endswith(".py"):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        if r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project" in content:
            print(f"Updating {filename}")
            new_content = content.replace(r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project", r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(new_content)
