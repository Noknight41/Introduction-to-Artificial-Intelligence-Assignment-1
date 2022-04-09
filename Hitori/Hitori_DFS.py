from turtle import right
from matplotlib.pyplot import flag
import numpy as np
from collections import Counter
from collections import defaultdict
import time
import sys


a = 0 


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    def addEdge(self,u,v):
        self.graph[u].append(v)
    def disconnected(self, s, num):
        visited = [False] * (max(self.graph) + 1)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            s = queue.pop(0)
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        if(visited.count(True) != num): return True
        else: return False
            
def solve(array):
    solveSub(array, 0)

def solveSub(array, index):
    length = len(array)
    if(index == length * length):
        return checkSolution(array)
        
    flag1 = False
    flag2 = False
    temp = []
    if(list(array[int(index/length)]).count(array[int(index / length)][index % length]) == 1):
        flag1 = True
    for i in range(len(array)):
        temp.append(array[i][index % length])
    if(temp.count(array[int(index / length)][index % length]) == 1):
        flag2 = True
    if(flag1 and flag2):
        return solveSub(array, index+1)

    else:
        if(solveSub(array, index+1)):
            return True
        else:
            array_temp = array.copy()
            array_temp[int(index / length)][index % length] =  - array_temp[int(index / length)][index % length]
            return solveSub(array_temp, index+1)

def isInValidPointDark(array, i,j):
    top = array[i-1][j] if i > 0 else 1
    bot = array[i+1][j] if i < len(array) - 1 else 1
    left = array[i][j-1] if j > 0 else 1
    right = array[i][j+1] if j < len(array) - 1 else 1
    if(top < 0 or bot < 0 or left < 0 or right < 0):
        return True
    else: return False
    
def isInValidPointWhite(array, i,j):
    top = array[i-1][j] if i > 0 else -1
    bot = array[i+1][j] if i < len(array) - 1 else -1
    left = array[i][j-1] if j > 0 else -1
    right = array[i][j+1] if j < len(array) - 1 else -1
    if top < 0 and bot < 0 and left < 0 and right < 0 :
        return True
    else: return False

def checkSolution(array):
    global a
    a += 1
    print('Loading ', a)
    for i in array:
        result = list(filter(lambda x: x >0, i))
        if(len(list(Counter(result))) != len(result)): return False
    for j in range(len(array)):
        temp = []
        for i in range(len(array)):
            temp.append(array[i][j])
        result = list(filter(lambda x: x >0, temp))
        if(len(list(Counter(result))) != len(result)): return False
    g =  Graph()
    start = 0
    num = 0
    for i in range(len(array)):
        for j in range(len(array)):
            if(array[i][j] < 0):
                if(isInValidPointDark(array,i,j)): return False
            else:
                if(isInValidPointWhite(array,i,j)): return False
                num += 1
                if(start == 0): start = i*len(array)+j
                top = (i-1)*len(array)+j if i > 0 and array[i-1][j] > 0 else -1
                bot = (i+1)*len(array)+j   if i < len(array) - 1 and array[i+1][j] > 0 else -1
                left = i*len(array)+j-1   if j > 0 and array[i][j-1] > 0 else -1
                right = i*len(array)+j+1   if j < len(array) - 1 and array[i][j+1] > 0 else -1
                
                if(top != -1):
                    g.addEdge(i*len(array)+j,top)
                if(bot  != -1):
                    g.addEdge(i*len(array)+j,bot)
                if(left  != -1):
                    g.addEdge(i*len(array)+j,left)
                if(right  != -1):
                    g.addEdge(i*len(array)+j,right)
 
    if(g.disconnected(start,num)): 
        return False
    # else:
        
    #     return False
    printArray(array)
    a = 0
    return True

def load(path):
    array = np.loadtxt(path, dtype=int)
    return array

def printArray(array):
    for i in range(len(array)):
        temp = ''
        temp1 = ''
        for j in range(len(array)):
            if(array[i][j] > 0 ): temp += '  ' + str(array[i][j]) 
            else: temp +=  ' ' + str(array[i][j]) 
            if(array[i][j] > 0 ): temp1 += ' ' + 'o' 
            else: temp1 +=  ' ' + 'x'
        print(temp + '   ' + temp1)




def main(argv):
    for testCase in argv:
        start_time = time.time()
        array = load(testCase)
        solve(array)
        print("--- %s seconds ---" % (time.time() - start_time))
        print('\n')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        main(["test_1.txt"])
