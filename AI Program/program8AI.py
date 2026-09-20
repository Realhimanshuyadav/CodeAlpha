def get_moves(a, b, A, B):
    moves = []
    if a < A: moves.append(((A, b), "Fill Jug A"))
    if b < B: moves.append(((a, B), "Fill Jug B"))
    if a > 0: moves.append(((0, b), "Empty Jug A"))
    if b > 0: moves.append(((a, 0), "Empty Jug B"))
    if a > 0 and b < B:
        t = min(a, B - b)
        moves.append(((a - t, b + t), f"Pour {t}L from A → B"))
    if b > 0 and a < A:
        t = min(b, A - a)
        moves.append(((a + t, b - t), f"Pour {t}L from B → A"))
    return moves

def dls(state, depth, A, B, goal, visited):
    if goal in state: return [(state, "Goal Reached")]
    if depth == 0: return None
    for (nxt, action) in get_moves(*state, A, B):
        if nxt not in visited:
            visited.add(nxt)
            path = dls(nxt, depth - 1, A, B, goal, visited)
            if path: return [(state, action)] + path
    return None

def ids(A, B, goal, max_depth):
    start = (0, 0)
    for d in range(max_depth + 1):
        path = dls(start, d, A, B, goal, {start})
        if path: return path
    return None

# ---- User Input ----
A = int(input("Enter capacity of Jug A: "))
B = int(input("Enter capacity of Jug B: "))
goal = int(input("Enter target amount to measure: "))
max_depth = int(input("Enter maximum search depth : "))

path = ids(A, B, goal, max_depth)
if not path:
    print("No solution found within given depth.")
else:
    print("\n Solution Path:")
    for i, (state, action) in enumerate(path):
        a, b = state
        print(f"Step {i}: Jug A = {a}L, Jug B = {b}L → {action}")
    print(f"\nTotal steps: {len(path)-1}")
