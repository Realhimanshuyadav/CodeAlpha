import heapq

def best_first(graph, h, start, goal):
    pq=[(h[start], start, [start])]
    visited=set()
    while pq:
        _, node, path = heapq.heappop(pq)
        if node==goal: return path
        if node in visited: continue
        visited.add(node)
        for n in graph[node]:
            if n not in visited:
                heapq.heappush(pq,(h[n],n,path+[n]))

# Graph
graph={'H':['I','M'],
'I':['A','N'],
'M':['S','h','U'],
'A':[],
'N':[],
'S':[],
'h':[],
'U':[]}

# Heuristics
h={'H':10,
   'I':9,
   'M':8,
   'A':7,
   'N':6,
   'S':5,
   'h':3,
   'U':0}

print("Path:", " -> ".join(best_first(graph,h,'H','U')))
