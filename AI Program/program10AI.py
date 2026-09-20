# --- Build Knowledge Base from User Input ---
fathers = {}

n = int(input("Enter number of father-child pairs: "))
for _ in range(n):
    f = input("Enter father's name: ")
    c = input(f"Enter {f}'s child name (or leave blank if unknown): ")
    fathers[f] = c if c else None


# --- Inference Function ---
def find_grandparents(fathers):
    grandparents = {}
    for father, child in fathers.items():
        if child and child in fathers and fathers[child]:
            grandparents[father] = fathers[child]
    return grandparents


# --- Infer Grandparents ---
grandparents = find_grandparents(fathers)


# --- Display Output ---
print("\nFathers:")
for f, c in fathers.items():
    if c:
        print(f"{f} is father of {c}")
    else:
        print(f"{f} is father of ?")

print("\nGrandparents:")
if grandparents:
    for g, gc in grandparents.items():
        print(f"{g} is grandparent of {gc}")
else:
    print("No grandparent relationships inferred.")
