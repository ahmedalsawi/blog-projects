
import random

class Graph:
    def __init__(self, V):
        self.V = V
        self.graph = [[] for i in range(V)]

    def connect(self, n1,n2, w):
        self.graph[n1].append((n2,w))
        self.graph[n2].append((n1,w))

    def checkAllConncted(self):
        for v in self.graph:
            if len(v) == 0: # one node not connected
                return False
        return True

class Prim(Graph):
    def __init__(self,V):
        Graph.__init__(self,V)
        self.mst  = Graph(self.V)

        
    def MST(self):
        mstSet = []
        # initial random node
        start = random.randint(0, self.V-1)
        mstSet.append(start)
        print(f">> Starting at node {start}")
        total = 0
        run = True
        while run:
            # Get edges from connected nodes
            edge= ()
            
            value = float('inf')
            for n1 in mstSet:
                for (n2,w) in self.graph[n1]:
                    if w < value and (not n2 in mstSet):
                        edge = (n1,n2,w)
                        value = w
                        
            
            mstSet.append(edge[1])
            total += edge[2]
            print(f"edge={edge}")
            # connect the node 
            self.mst.connect(*edge)
            # check if all nodes are in the MST
            run = len(mstSet) != self.V
        print(f"total weight={total}")
        


def main():
    g = Prim(9)
    g.connect(0,1,4)
    g.connect(0,7,8)
    g.connect(1,7,11)
    g.connect(1,2,8)
    g.connect(7,8,7)
    g.connect(7,6,1)
    g.connect(2,8,2)
    g.connect(2,5,4)
    g.connect(2,3,7)
    g.connect(8,6,6)
    g.connect(6,5,2)
    g.connect(3,5,14)
    g.connect(3,4,9)
    g.connect(5,4,10)
    g.MST()

    for v in g.mst.graph:
        print(f"vertix={v}")

if __name__ == "__main__":
    main()
