"""
https://www2.cs.duke.edu/courses/cps100r/spring18/notes/0228/13-percolation-uf.pdf
"""

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

from random import randrange

import argparse
import logging


def xy_to_idx(x,y,N):
    return x*N + y

def idx_to_xy(idx, N):
    (x,y) = divmod(idx, N)
    return (x,y)

"""
retrun list of tuples for points around (x,y) cell
"""
def isOnGrid(x,y,N):
    return (x >=0) and (y >=0) and (x < N) and (y < N)
def neighbours(x,y,N):
    l = []
    # for xx in [-1,1]:
    #     for yy in [-1,1]:
    #         if xx == 0 and yy == 0:
    #             continue
    #         if isOnGrid(x + xx, y + yy,N):
    #             l.append((x+xx,y+yy))
    xx = 0
    for yy in [-1,1]:
        if isOnGrid(x + xx, y + yy,N):
            l.append((x+xx,y+yy))

    yy = 0
    for xx in [-1,1]:
        if isOnGrid(x + xx, y + yy,N):
            l.append((x+xx,y+yy))  
    return l

class QuickFind():
    def __init__(self, N):
        self.N = N
        self.id = []
        for i in range(N):
            self.id.append(i)

    def union(self, p ,q):
        logging.info(f"UF: Connecting {p} and {q}")
        new_id = self.id[q]
        old_id = self.id[p]
        for i in range(self.N):
            if (self.id[i] == old_id):
                self.id[i] = new_id
    def find(self, p):
        return self.id[p]
    def connected(self,p,q):
        return self.find(p) == self.find(q)


class QuickUnion():
    def __init__(self, N):
        self.N = N
        self.id = []
        for i in range(N):
            self.id.append(i)

    def union(self, p ,q):
        logging.info(f"UF: Connecting {p} and {q}")
        self.id[self.find(p)] = self.find(q)
        logging.info(f"id={self.id}")
    def find(self, p):
        root = self.id[p]
        while (not root ==  self.id[root]):
            root = self.id[root]
        return root
    def connected(self,p,q):
        return self.find(p) == self.find(q)

class Percolation():
    def __init__(self, N):
        self.N      = N
        self.grid   = np.random.choice(a=[False], size=(N, N))

        # Create UF nodes
        self.TOP    = (N * N)
        self.BOTTOM = (N * N) + 1
        uf = QuickUnion((N*N)+2) # N*N nodes and 2 for top and bottom nodes
        # Connect top and bottom nodes
        for i in range(self.N):
            uf.union(xy_to_idx(0,   i,N), self.TOP)
            uf.union(xy_to_idx(N-1, i,N), self.BOTTOM)
        self.uf = uf

    def open_site(self):
        # generate random cell and copen it
        idx = randrange(self.N * self.N)
        (x,y) = idx_to_xy(idx, self.N)

        if self.grid[x][y] == False:
            logging.info(f"Opening cell ({x},{y})")
            self.grid[x][y] = True
            
            # connect to surrouding cells
            for cell in neighbours(x,y,self.N):
                if self.grid[cell[0]][cell[1]] == True:
                    self.uf.union(xy_to_idx(x,y,self.N), xy_to_idx(cell[0], cell[1],self.N))

    def is_perculatres(self):
        return self.uf.connected(self.TOP, self.BOTTOM)

    # public API
    def run(self):
        while(not self.is_perculatres()):
            self.open_site()
            yield self.grid

    ## TODO Debug this
    # def animate(self):
    #     fig, ax = plt.subplots()
    #     mat = ax.matshow(self.grid)   
    #     ani = animation.FuncAnimation(fig, mat.set_data, self.run, interval=500, repeat=False)
    #     plt.show()

    def show(self):
        fig, ax = plt.subplots()
        mat = ax.matshow(self.grid)
        plt.show()

    def batch(self):
        for grid in self.run():
            logging.info(f" Grid after open cell \n{grid}")
    
    def stats(self):
        open_cells = np.sum(self.grid)
        self.per = open_cells/ (self.N * self.N)
        logging.warning(f"Percentage={self.per}")
        return self.per

def main():
    parser = argparse.ArgumentParser(description='Perculation with Union-Find')

    parser.add_argument('N', type=int, help='Grid Size')
    parser.add_argument('I', type=int, help='Iterations')
    args = parser.parse_args()
    for  i in range(args.I):
        p = Percolation(args.N)
        p.batch()
        p.stats()
        p.show()

if __name__ == "__main__":
    main()