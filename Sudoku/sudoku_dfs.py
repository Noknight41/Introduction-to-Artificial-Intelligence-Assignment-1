import numpy as np
import math
import copy
import time
import sys
import tracemalloc
import linecache
import os

a = 0

# def display_top(snapshot, key_type='lineno', limit=3):
#     snapshot = snapshot.filter_traces((
#         tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
#         tracemalloc.Filter(False, "<unknown>"),
#     ))
#     top_stats = snapshot.statistics(key_type)

#     print("Top %s lines" % limit)
#     for index, stat in enumerate(top_stats[:limit], 1):
#         frame = stat.traceback[0]
#         # replace "/path/to/module/file.py" with "module/file.py"
#         filename = os.sep.join(frame.filename.split(os.sep)[-2:])
#         print("#%s: %s:%s: %.1f KiB"
#               % (index, filename, frame.lineno, stat.size / 1024))
#         line = linecache.getline(frame.filename, frame.lineno).strip()
#         if line:
#             print('    %s' % line)

#     other = top_stats[limit:]
#     if other:
#         size = sum(stat.size for stat in other)
#         print("%s other: %.1f KiB" % (len(other), size / 1024))
#     total = sum(stat.size for stat in top_stats)
#     print("Total allocated size: %.1f B" % (total))

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
    def load(self, path, print = True):
        with open('demo_step_by_step_dfs.txt','w') as f: pass
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
    
    def solve(self, print = True):
        self.start.preChecking()
        self.process()
        if print == True:
            self.printPuzzle(self.solution.data)
        return

    def process(self):
        self.solved = 0 # Flag when finished
        self.fill(0, 0, self.start) # 
    
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
            self.demoWritePuzzle(node.data)
            for value in range(1, self.n + 1):
                if node.legalValue(value, i, j):
                    new_node = Node(copy.copy(node.m), copy.copy(node.data), self.copyRCB(node.row), self.copyRCB(node.column), self.copyRCB(node.block))
                    new_node.addTo(value, i, j)
                    if j == self.n - 1:
                        if i == self.n - 1:
                            self.solution = new_node
                            self.solved = 1
                            self.demoWritePuzzle(new_node.data)
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
                print("------------------------")
            for j in range(len(data[i])):
                if j  % self.m == 0:
                    line += "| "
                line += str(data[i,j]) + " "
            line += "| "
            print(line)
        print("------------------------")
    
    def demoWritePuzzle(self, data):
        global a
        a += 1
        with open('demo_step_by_step_dfs.txt', 'a') as f:
            f.writelines("Step " + str(a) + '\n')
            for i in range(len(data)):
                line = ""
                if i % self.m == 0:
                    f.writelines("------------------------" + '\n')
                for j in range(len(data[i])):
                    if j  % self.m == 0:
                        line += "| "
                    line += str(data[i,j]) + " "
                line += "| "
                f.writelines(line + '\n')
            f.writelines("------------------------" + '\n\n')

# Run the program
def main(argv):
    start_time = time.time()
    puzzle = Sudoku()
    path = ''
    for testCase in argv:
        # print(testCase)
        puzzle.load(testCase, True)
        # tracemalloc.start()
        puzzle.solve(True)
        print("--- %s seconds ---" % (time.time() - start_time))
        # snapshot = tracemalloc.take_snapshot()
        # tracemalloc.stop()
        # display_top(snapshot)
        print('\n')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        main(["test_1.txt"])




