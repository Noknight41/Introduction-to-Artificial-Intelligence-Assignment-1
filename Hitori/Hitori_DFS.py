from turtle import right
import numpy as np
from collections import Counter
import time
start_time = time.time()

a = 0 

def solve(array):
    solveSub(array, 0)

def solveSub(array, index):
    length = len(array)
    if(index == length * length):
        return checkSolution(array)
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
    # print(array)
    # print('Loading ', a)
    # if(a == 20): return True
    for i in array:
        result = list(filter(lambda x: x >0, i))
        if(len(list(Counter(result))) != len(result)): return False
    for j in range(len(array)):
        temp = []
        for i in range(len(array)):
            temp.append(array[i][j])
        result = list(filter(lambda x: x >0, temp))
        if(len(list(Counter(result))) != len(result)): return False

    for i in range(len(array)):
        for j in range(len(array)):
            if(array[i][j] < 0):
                if(isInValidPointDark(array,i,j)): return False
            else:
                if(isInValidPointWhite(array,i,j)): return False
    printArray(array)
    return True


def load(path):
    array = np.loadtxt(path, dtype=int)
    return array

def printArray(array):
    for i in range(len(array)):
        temp = ''
        for j in range(len(array)):
            if(array[i][j] > 0 ): temp += '  ' + str(array[i][j]) 
            else: temp +=  ' ' + str(array[i][j]) 
        print(temp)

array = load("test_2.txt")
solve(array)
print("--- %s seconds ---" % (time.time() - start_time))