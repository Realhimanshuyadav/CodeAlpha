import re
# Get user input 
expr = input("Enter logical expression (use &, |, ~, ->): ").strip()
# Extract variable names (A, B, C, etc.)
vars_found = sorted(set(re.findall(r"[A-Za-z]+", expr)))
values = {}
#Ask user for truth values 
for v in vars_found:
    val = input(f"Enter truth value for {v} (T/F): ").strip().upper()
    values[v] = True if val == 'T' else False
# Replace symbols with Python equivalents
expr_py = expr
expr_py = expr_py.replace("->", " <= ")  
expr_py = expr_py.replace("&", " and ")
expr_py = expr_py.replace("|", " or ")
expr_py = expr_py.replace("~", " not ")
expr_py = expr_py.replace("<= ", " <= ") 
# Replace variables
for v in vars_found:
    expr_py = re.sub(rf"\b{v}\b", str(values[v]), expr_py)
#Evaluate implication (A -> B == (not A or B)) 
expr_py = re.sub(r'([A-Za-z0-9\)\]]+)\s*<=\s*([A-Za-z0-9\(]+)', r'(not (\1) or (\2))', expr_py)
#Evaluate the expression
try:
    result = eval(expr_py)
    print(f"\nExpression: {expr}")
    print(f"Result: {result}")
except Exception as e:
    print("Invalid logical expression.")
