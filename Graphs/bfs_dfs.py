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
        visited[start] = True
        print(f"DFS Node = {start}")

        while len(s) != 0:
            adjVertix = None

            for (n2,w) in self.graph[s[-1]]:
                if (visited[n2] == False):
                    adjVertix= n2

            if adjVertix is None:
                s.pop()
            else:
                visited[adjVertix] = True
                print(f"DFS Node = {adjVertix}")
                s.append(adjVertix)




class UndirectedGraph(Graph):
    def __init__(self, V):
        self.V = V
        self.graph = [[] for i in range(V)]

    def connect(self, n1,n2, w):
        self.graph[n1].append((n2,w))
        self.graph[n2].append((n1,w))

class DirectedGraph(Graph):
    def __init__(self, V):
        self.V = V
        self.graph = [[] for i in range(V)]

    def connect(self, n1,n2, w):
        self.graph[n1].append((n2,w))



        
def main():
    g = DirectedGraph(4)
    g.connect(1,2,0)
    g.connect(0,2,0)
    g.connect(0,1,0)
    g.connect(2,0,0)
    g.connect(2,3,0)
    g.connect(3,3,0)
    print('>>>>>>>>> BFS')
    g.BFS(2)
    print('>>>>>>>>> DFS')
    g.DFS(2)

    print('===================')
    g1 = UndirectedGraph(6)
    g1.connect(0,1,0)
    g1.connect(0,2,0)
    g1.connect(1,4,0)
    g1.connect(1,3,0)
    g1.connect(2,4,0)
    g1.connect(3,4,0)
    g1.connect(3,5,0)
    g1.connect(4,5,0)
    print('BFS')
    g1.BFS(0)
    print('DFS')
    g1.DFS(0)
if __name__ == "__main__":
    main()
