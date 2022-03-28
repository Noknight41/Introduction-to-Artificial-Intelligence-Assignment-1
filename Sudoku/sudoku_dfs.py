import numpy as np
import math
import copy
import time
import tracemalloc
import linecache
import os

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f B" % (total))

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
    
    # Convert string character to int character
    def convert(self, file_list):
        result = []
        for x in file_list:
            if x == "0":
                result += [0]
            if x == "1":
                result += [1]
            if x == "2":
                result += [2]
            if x == "3":
                result += [3]
            if x == "4":
                result += [4]
            if x == "5":
                result += [5]
            if x == "6":
                result += [6]
            if x == "7":
                result += [7]
            if x == "8":
                result += [8]
            if x == "9":
                result += [9]
            if x == "A":
                result += [10]
            if x == "B":
                result += [11]
            if x == "C":
                result += [12]
            if x == "D":
                result += [13]
            if x == "E":
                result += [14]
            if x == "F":
                result += [15]
            if x == "G":
                result += [16]
        print(result)
        return result
                
    # Load Sudoku from txt file
    def load(self, path, print = True):
        with open(path, "r") as f:
            file = np.loadtxt(f).astype(int)
            self.n = len(file[0])
            self.m = int(math.sqrt(self.n))
            if print == True:
                self.printPuzzle(file)
            r = []
            c = []
            b = []
            for i in range(0, self.n):
                r.append(list(range(1, self.n + 1)))
                c.append(list(range(1, self.n + 1)))
                b.append(list(range(1, self.n + 1)))
            self.start = Node(self.m , file, r, c, b)
        return

    def process(self):
        self.solved = 0
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
        if self.solved == 1:
            return
        if node.data[i][j] == 0:
            for value in range(1, self.n + 1):
                if node.legalValue(value, i, j):
                    new_node = Node(copy.copy(node.m), copy.copy(node.data), self.copyRCB(node.row), self.copyRCB(node.column), self.copyRCB(node.block))
                    new_node.addTo(value, i, j)
                    if j == self.n - 1:
                        if i == self.n - 1:
                            self.solution = new_node
                            self.solved = 1
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
            
    def solve(self, print = True):
        self.start.preChecking()
        self.process()
        if print == True:
            self.printPuzzle(self.solution.data)
        return

# Start
tracemalloc.start()
# start_time = time.time()

puzzle = Sudoku()
puzzle.load("test_14.txt", False)
puzzle.solve(False)
# print("--- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
snapshot = tracemalloc.take_snapshot()
display_top(snapshot)



