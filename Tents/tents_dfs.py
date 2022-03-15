import numpy as np
import math
import copy

class Tents:
    def __init__(self):
        self.solved = 0
    
    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            file = np.loadtxt(f).astype(int)
            self.n = len(file[0])
            rowConstraint = file[self.n]
            columnConstraint = file[self.n + 1]
        return file[:self.n], rowConstraint, columnConstraint

    def treeHasTent(self, mapTents, i, j):
        neighbors = [[i, j+1],[i,j-1],[i+1,j],[i-1,j]]
        for neighbor in neighbors:
            if neighbor[0] < 0 or neighbor[0] > self.n - 1 or neighbor[1] < 0 or neighbor[1] > self.n - 1:
                continue
            if mapTents[neighbor[0]][neighbor[1]] == -1:
                return True
        return False
            
    def allTreeHasTent(self, mapTents):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if mapTents[i][j] == 1 and (not self.treeHasTent(mapTents, i, j)):
                    return False
        return True
                    
    def legalPlace(self, mapTents, i, j):
        surround = [[i, j+1],[i,j-1],[i+1,j+1],[i-1,j-1],
                    [i+1,j],[i-1,j],[i+1,j-1],[i-1,j+1]]
        for neighbor in surround:
            if neighbor[0] < 0 or neighbor[0] > self.n - 1 or neighbor[1] < 0 or neighbor[1] > self.n - 1:
                continue
            if mapTents[neighbor[0]][neighbor[1]] == -1:
                return False
        return True
    
    def checkAndPlace(self, mapTents, row, col, i, j):
        if self.solved == 0:
            if j == self.n:
                if row[i] != 0:
                    return
                else:
                    if i == self.n - 1:
                        if self.allTreeHasTent(mapTents):
                            self.solution = mapTents
                            self.solved = 1
                        return
                    else:
                        self.checkAndPlace(mapTents, row, col, i + 1, 0)
                        return
            if mapTents[i][j] == 0: # Empty Plot 
                if row[i] > 0 and col[j] > 0 and self.legalPlace(mapTents, i, j): # Legal to Place Tents
                    new_map = mapTents.copy()
                    new_row = row.copy()
                    new_col = col.copy()
                    new_map[i][j] = -1
                    new_row[i] -= 1
                    new_col[j] -= 1
                    self.checkAndPlace(new_map, new_row, new_col, i, j + 1)
            # Bypass the plot
            self.checkAndPlace(mapTents, row, col, i, j + 1)
            return
        else:
            return # Have found solution, other branches stop searching
            
    def solve(self, path):
        mapTents, rowConstraint, columnConstraint = self.load(path)
        self.checkAndPlace(mapTents, rowConstraint, columnConstraint, 0, 0)
        print("-----------")
        print(self.solution)
        

tents = Tents()
tents.solve("test_2.txt")