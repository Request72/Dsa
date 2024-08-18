class DSU:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        rootU = self.find(u)
        rootV = self.find(v)
        
        if rootU != rootV:
            if self.rank[rootU] > self.rank[rootV]:
                self.parent[rootV] = rootU
            elif self.rank[rootU] < self.rank[rootV]:
                self.parent[rootU] = rootV
            else:
                self.parent[rootV] = rootU
                self.rank[rootU] += 1

def can_requests_be_approved(n, restrictions, requests):
    dsu = DSU(n)
    
    restricted = [set() for _ in range(n)]
    for u, v in restrictions:
        restricted[u].add(v)
        restricted[v].add(u)
    
    results = []

    for u, v in requests:
        if dsu.find(u) == dsu.find(v):
            results.append("denied")
        else:
            can_approve = True
            for restricted_house in restricted[u]:
                if dsu.find(restricted_house) == dsu.find(v):
                    can_approve = False
                    break
            if can_approve:
                results.append("approved")
                dsu.union(u, v)
            else:
                results.append("denied")
    
    return results

n = 5
restrictions = [[0, 1], [1, 2], [2, 3]]
requests = [[0, 4], [1, 2], [3, 1], [3, 4]]
print(can_requests_be_approved(n, restrictions, requests))
