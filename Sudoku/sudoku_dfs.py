import numpy as np
import math
import copy

class Node:
    def __init__(self, size, data, row, column, block):
        self.m = size
        self.data = data
        self.row = row
        self.column = column
        self.block = block
            
    def addTo(self, value, i, j):
        if value > 0 and value < self.m * self.m + 1:
            self.data[i][j] = value
            self.row[i].remove(value)
            self.column[j].remove(value)
            self.block[ (i // self.m) * self.m + j // self.m ].remove(value)
        
    def preChecking(self):
        for i in range(0, self.m * self.m):
            for j in range(0, self.m * self.m):
                if self.data[i][j] != 0:
                    t = self.data[i][j]
                    self.addTo(t, i, j)
    
    def legalValue(self, value, i, j):
        return value in self.row[i] and value in self.column[j] and value in self.block[(i // self.m) * self.m + j // self.m]


class Sudoku:
    def __init__(self):
        pass
    
    # Load Sudoku from txt file 
    def load(self, path):
        with open(path, "r") as f:
            val = np.loadtxt(f).astype(int)
            self.n = int(math.sqrt(len(val)))
            self.m = int(math.sqrt(self.n))
            values = val.reshape((self.m * self.m, self.m * self.m))
            self.printPuzzle(values)
            r = []
            c = []
            b = []
            for i in range(0, self.n):
                r.append(list(range(1, self.n + 1)))
                c.append(list(range(1, self.n + 1)))
                b.append(list(range(1, self.n + 1)))
            self.start = Node(self.m , values, r, c, b)
        return

    def process(self):
        self.fill(0, 0, self.start)
    
    def copyRCB(self, llist):
        result = []
        for i in llist:
            r = []
            for x in i:
                r.append(x)
            result.append(r)
        return result
    
    def fill(self, i, j, node):
        if node.data[i][j] == 0:
            for value in range(1, self.n + 1):
                if node.legalValue(value, i, j):
                    new_node = Node(copy.copy(node.m), copy.copy(node.data), self.copyRCB(node.row), self.copyRCB(node.column), self.copyRCB(node.block))
                    new_node.addTo(value, i, j)
                    if j == self.n - 1:
                        if i == self.n - 1:
                            self.solution = new_node
                        else:
                            self.fill(i + 1, 0, new_node)
                    else:
                        self.fill(i, j + 1, new_node)
        else:
            new_node = Node(copy.copy(node.m), copy.copy(node.data), self.copyRCB(node.row), self.copyRCB(node.column), self.copyRCB(node.block))
            if j == self.n - 1:
                if i == self.n - 1:
                    self.solution = node
                else:
                    self.fill(i + 1, 0, new_node)
            else:
                self.fill(i, j + 1, new_node)
    
            
    
    def printPuzzle(self, data):
        print("\n")
        for i in range(len(data)):
            line = ""
            if i % self.m == 0:
                print("---------------------")
            for j in range(len(data[i])):
                if j  % self.m == 0:
                    line += "| "
                line += str(data[i,j])+" "
            print(line)
            
    def solve(self):
        self.start.preChecking()
        self.process()
        self.printPuzzle(self.solution.data)
        return

puzzle = Sudoku()
puzzle.load("test_2.txt")
puzzle.solve()
