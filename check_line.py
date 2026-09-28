with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_script = False
script_lines = []
for line in lines:
    if "<script type=\"text/babel\">" in line:
        in_script = True
        continue
    if "</script>" in line and in_script:
        break
    if in_script:
        script_lines.append(line)

print("Line 384:", script_lines[383].strip())
print("Line 385:", script_lines[384].strip())
print("Line 386:", script_lines[385].strip())
print("Line 387:", script_lines[386].strip())
print("Line 388:", script_lines[387].strip())
print("Line 389:", script_lines[388].strip())
print("Line 390:", script_lines[389].strip())
