"""
http://www.cs.qub.ac.uk/~I.Spence/SuDoku/SuDoku.html
http://cse.unl.edu/~choueiry/S17-235H/files/SATslides02.pdf
"""

import pycosat 
import numpy as np

N = 10

def ijk_idx(i,j,k):
    return (i * N * N + j * N + k)

def idx_ijk(idx):
    idx = idx 
    v, k = divmod(idx, N)
    v, j = divmod(idx, N)
    v, i = divmod(idx, N)
    return (i,j,k)

def create_cnf():
    cnf = []
    # cells
    for i in range(1,10):
        for j in range(1,10):
            cl = [ijk_idx(i,j,k) for k in range(1,10)]
            cnf.append(cl)

    for i in range(1,10):
        for j in range(1,10):
            for x in range(1,9):
                for y in range(x+1,10):
                    cl = [-1*ijk_idx(i,j,x), -1*ijk_idx(i,j,y)]
                    cnf.append(cl)
    # rows
    for i in range(1,10):
        for n in range(1,10):
            cl = [ijk_idx(i,j,n) for j in range(1,10)]
            cnf.append(cl)
            # for j1 in range(1,9):
            #     for j2 in range(x+1,10):
            #         cl = [-1*ijk_idx(i,j1,n), -1*ijk_idx(i,j2,n)]
            #         cnf.append(cl)
    # cols
    for j in range(1,10):
        for n in range(1,10):
            cl = [ijk_idx(i,j,n) for i in range(1,10)]
            cnf.append(cl)
            # for i1 in range(1,9):
            #     for i2 in range(x+1,10):
            #         cl = [-1*ijk_idx(i1,j,n), -1*ijk_idx(i1,j,n)]
            #         cnf.append(cl)
    # 3x3 Box
    t = []
    for i in range(1,4):
        for j in range(1,4):
            t.append((i,j))
    for r in range(0,3):
        for s in range(0,3):
            for n in range(1,10):
                cl = [ijk_idx(3*r + i, 3*s+j, n) for (i,j) in t]
                cnf.append(cl)
    return cnf

class Sudoku():
    def __init__(self):
        self.cnf = create_cnf()
        self.grid = np.zeros((9,9))

    def initial(self, init):
        for (i,j,k) in init:
            cl = [ijk_idx(i,j,k)]
            self.cnf.append(cl)
            self.grid[i-1][j-1] = k
        print("Sudoku After initialization\n===========================")
        print(self.grid)

    def solve(self):
        sat = pycosat.solve(self.cnf)
        if isinstance(sat, str):
            print("unsolved")
        else:
            for i in range(1,10):
                for j in range(1,10):
                    for k in range(1,10):
                        if ijk_idx(i,j,k) in sat:
                            self.grid[i-1][j-1] = k
            print("Sudoku After Solving\n===========================")
            print(self.grid)
            return self.grid
        

init = [
    (2,2,8),
    (2,3,9),
    (2,4,4),
    (2,5,1),
    (3,3,6),
    (3,4,7),
    (3,7,1),
    (3,8,9),
    (3,9,3),
    (4,1,2),
    (4,7,7),
    (5,1,3),
    (5,2,4),
    (5,4,6),
    (5,8,1),
    (6,4,9),
    (6,9,5),
    (7,5,2),
    (7,8,5),
    (8,1,6),
    (8,2,5),
    (8,5,4),
    (8,8,2),
    (9,1,7),
    (9,2,3),
    (9,4,1)
]
def main():
    s = Sudoku()
    s.initial(init)
    s.solve()

if __name__ == "__main__":
    main()