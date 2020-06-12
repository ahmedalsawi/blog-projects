
class Dijkstra:
    """
    Implementation based on algorithm in 
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    def __init__(self, V):
        self.V = V
        self.graph = [[] for i in range(V)]

    def connect(self, n1,n2, w):
        self.graph[n1].append((n2,w))
        self.graph[n2].append((n1,w))

    def shortestPath(self, n1, n2=None):
        unvisited = [True] * self.V

        distance = [ float('inf') ] * self.V
        distance[n1] = 0

        current = n1

        run  = True
        while run:
            #print(f">>>> current={current}")
            # iterate the neighbours
            for neighbour in self.graph[current]:
                n = neighbour[0]
                w = neighbour[1]
                if unvisited[n]:
                    # Loop over neighbours
                    #print(f"    >>>> neighbour={n} weight={w}")
                    new_dist = distance[current] + w

                    if  new_dist < distance[n]:
                        #print(f"        >>>> updated distance {new_dist}")
                        distance[n] = new_dist
                    
            unvisited[current] = False

            # check for algorithm termination and calculate the new "current"
            if n2 is None:
                run =  (True in unvisited) 
            else:
                run = (unvisited[n2] == True)
            
            value = float('inf')
            for v in range(self.V):
                if distance[v] < value and unvisited[v] == True:
                    value = distance[v]
                    n_current = v
            
            current = n_current

        print(distance)
            

def main():
    g = Dijkstra(9)
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
    g.shortestPath(0,7)
    
    g.shortestPath(0)
    g.shortestPath(1)
if __name__ == "__main__":
    main()
