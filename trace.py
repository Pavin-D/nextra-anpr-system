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

def check(lines):
    stack_b = []
    for i, line in enumerate(lines):
        # Extremely basic check ignoring strings
        line = line.split("//")[0]
        for j, char in enumerate(line):
            if char == '{': stack_b.append((i+1, j))
            elif char == '}': 
                if stack_b: stack_b.pop()
                else: print(f"Extra }} at {i+1}:{j}")
    print("Unclosed {: ", stack_b)

check(script_lines)
