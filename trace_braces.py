with open("test.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

def check(lines):
    stack_p = []
    stack_b = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '(': stack_p.append((i+1, j))
            elif char == ')': 
                if stack_p: stack_p.pop()
                else: print(f"Extra ) at {i+1}:{j}")
            elif char == '{': stack_b.append((i+1, j))
            elif char == '}': 
                if stack_b: stack_b.pop()
                else: print(f"Extra }} at {i+1}:{j}")
    
    print("Unclosed (: ", stack_p)
    print("Unclosed {: ", stack_b)

check(lines)
