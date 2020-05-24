import numpy as np
from scipy import signal
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

import argparse

class Conway():
    def __init__(self, N=10, G=1, shape='random'):
        self.N = N
        self.G = G
        self.grid = None
        self.neighbour = None

        if shape == 'random':
            self.grid = np.random.choice(a=[False, True], size=(N, N))
        else:
            self.grid = np.zeros((N, N), dtype='bool')

    def calc(self):
        W = np.array([[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])
        self.neighbour = signal.convolve2d(self.grid, W, 'same')
            
    def step(self):
        self.calc()
        for i in range(self.N):
            for j in range(self.N):
                # Rule1: if dead cell have exactly 3 surrouding living cell, it become a live
                if (self.grid[i,j] ==  0 and self.neighbour[i,j] == 3):
                    self.grid[i,j] = 1
                # Rule2 and Rule3: if living cell has > 3 or < 2 surrounding, it dies
                if (self.grid[i,j] == 1 and(self.neighbour[i,j] < 2 or self.neighbour[i,j] > 3) ):
                    self.grid[i,j] = 0
                # livining cell has 2 or 3, it staying alive
        return self.grid

    def generations(self):
        for g in range (self.G):
            yield self.step()


    def run(self):
        fig, ax = plt.subplots()
        mat = ax.matshow(self.grid)   
        ani = animation.FuncAnimation(fig, mat.set_data, self.generations, interval=500, repeat=False)
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Conway game of life')

    parser.add_argument('N', type=int, help='Grid Size')
    parser.add_argument('G', type=int, help='Generations Count')

    args = parser.parse_args()

    g = Conway(args.N,args.G)
    g.run()
    

if __name__ == "__main__":
    main()