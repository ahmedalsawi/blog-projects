class Graph:
    def BFS(self,start):
        # init queue and visited
        q = []
        visited = [False] * self.V
        # Added start node to queue and mark it visited
        q.append(start)
        visited[start] = True

        while len(q) !=0:
            current = q.pop(0)
            print(f"BFS Node {current}")
            for (n,w) in self.graph[current]:
                if visited[n] == False and (not n in q): # the second condition 
                    visited[n] = True
                    q.append(n)

    def DFS(self,start):
        # init stack and visited
        s = []
        visited = [False] * self.V

        s.append(start)
        
        while len(s) != 0:
            #print(f"stack={s}")
            v = s.pop()
            if visited[v] == False:
                visited[v] = True
                print(f"DFS Node = {v}")
                for (n2,w) in self.graph[v]:
                    s.append(n2)


class DirectedGraph(Graph):
    def __init__(self, V):
        self.V = V
        self.graph = [[] for i in range(V)]

    def connect(self, n1,n2, w):
        self.graph[n1].append((n2,w))


def main():
    pass
if __name__ == "__main__":
    main()
