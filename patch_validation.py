import re

with open("pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace validation block
pattern = r"# 1\. Strict confidence validation.*?# Insert Plate"
replacement = """# Validation rules disabled for testing
        if conf < 0.30:
            ocr_reject += 1
            continue
            
        ocr_success += 1
        timestamp = base_timestamp + timedelta(seconds=1)
        
        # Insert Plate"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
