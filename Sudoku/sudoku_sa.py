import random
import numpy as np
import math 
from random import choice
import matplotlib.pyplot as plt
import sys, time, tracemalloc, linecache, os

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

class Sudoku:    
    def __init__(self):
        pass
    
    # Load Sudoku from txt file 
    def load(self, path):
        with open(path, "r") as f:
            file = np.loadtxt(f).astype(int)
            self.n = len(file[0])
            self.m = int(math.sqrt(self.n))
            self.data = file.reshape((self.m * self.m, self.m * self.m))
        
    # Print the Sudoku
    def printSudoku(self, data):
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
    
    # Marking which value is non-changable 
    def FixSudokuValues(self, fixed_sudoku):
        for i in range (0, self.m ** 2):
            for j in range (0, self.m ** 2):
                if fixed_sudoku[i,j] != 0:
                    fixed_sudoku[i,j] = 1
        return fixed_sudoku

    # Heuristic Function    
    def CalculateNumberOfErrors(self, sudoku):
        numberOfErrors = 0 
        for i in range (0, self.m ** 2):
            numberOfErrors += self.CalculateNumberOfErrorsRowColumn(i ,i ,sudoku)
        return numberOfErrors

    # Calculating for Row + Column
    def CalculateNumberOfErrorsRowColumn(self, row, column, sudoku):
        numberOfErrors = (self.m ** 2 - len(np.unique(sudoku[:,column]))) + (self.m ** 2 - len(np.unique(sudoku[row,:])))
        return numberOfErrors

    # Create List of Index for Blocks 
    def CreateListofBlocks(self):
        finalListOfBlocks = []
        for r in range (0, self.m ** 2):
            tmpList = []
            block1 = [i + self.m * ((r) % self.m) for i in range(0, self.m)]
            block2 = [i + self.m * math.trunc((r) / self.m) for i in range(0, self.m)]
            for x in block1:
                for y in block2:
                    tmpList.append([x,y])
            finalListOfBlocks.append(tmpList)
        return finalListOfBlocks

    def RandomlyFillBlocks(self, sudoku, listOfBlocks):
        for block in listOfBlocks:
            for box in block:
                if sudoku[box[0],box[1]] == 0:
                    currentBlock = sudoku[block[0][0]:(block[-1][0] + 1), block[0][1]:(block[-1][1]+1)]
                    sudoku[box[0],box[1]] = choice([i for i in range(1, self.m ** 2 + 1) if i not in currentBlock])
        return sudoku

    # Sum of all boxes in 1 Blocks
    def SumOfOneBlock (self, sudoku, oneBlock):
        finalSum = 0
        for box in oneBlock:
            finalSum += sudoku[box[0], box[1]]
        return finalSum

    # Choose 2 Random boxes in 1 Block to swap 
    def chooseTwoRandomBoxes(self, fixedSudoku, block):
        while (1):
            firstBox = random.choice(block)
            secondBox = choice([box for box in block if box is not firstBox ])
            if fixedSudoku[firstBox[0], firstBox[1]] != 1 and fixedSudoku[secondBox[0], secondBox[1]] != 1:
                return([firstBox, secondBox])

    # Swap 2 boxes
    def swapBoxes(self, sudoku, boxesToFlip):
        proposedSudoku = np.copy(sudoku)
        placeHolder = proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]]
        proposedSudoku[boxesToFlip[0][0], boxesToFlip[0][1]] = proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]]
        proposedSudoku[boxesToFlip[1][0], boxesToFlip[1][1]] = placeHolder
        return proposedSudoku


    def ProposedState (self, sudoku, fixedSudoku, listOfBlocks):
        randomBlock = random.choice(listOfBlocks)
        boxesToFlip = self.chooseTwoRandomBoxes(fixedSudoku, randomBlock)
        proposedSudoku = self.swapBoxes(sudoku, boxesToFlip)
        return([proposedSudoku, boxesToFlip])


    def ChooseNewState (self, currentSudoku, fixedSudoku, listOfBlocks, temperature):
        proposal = self.ProposedState(currentSudoku, fixedSudoku, listOfBlocks)
        newSudoku = proposal[0]
        boxesToCheck = proposal[1]
        
        # Check before/after value
        curVal = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1], currentSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0], boxesToCheck[1][1], currentSudoku)
        newVal = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1], newSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0], boxesToCheck[1][1], newSudoku)
        
        costDifference = newVal - curVal
        rho = math.exp( -costDifference / temperature)
        if(np.random.uniform(1, 0, 1) < rho):
            return([newSudoku, costDifference])
        return([currentSudoku, 0])

    def ChooseNumberOfIterations(self, fixed_sudoku):
        numberOfIterations = 0
        for i in range (0, self.m ** 2):
            for j in range (0, self.m ** 2):
                if fixed_sudoku[i,j] == 0:
                    numberOfIterations += 1
        return numberOfIterations

    # Solve the sudoku
    def solve(self, printR = True):
        result = []
        solutionFound = 0
        decreaseFactor = 0.99
        stuckCount = 0
        fixedSudoku = np.copy(self.data)
        if printR == True:
            self.printSudoku(self.data)
        
        # Fixed Value and Assign Random Value to Sudoku
        fixedSudoku = self.FixSudokuValues(fixedSudoku)
        listOfBlocks = self.CreateListofBlocks()
        tmpSudoku = self.RandomlyFillBlocks(self.data, listOfBlocks)
        
        # temperature + Score + Iterations
        temperature = 1
        score = self.CalculateNumberOfErrors(tmpSudoku)
        iterations = self.ChooseNumberOfIterations(fixedSudoku)
        
        
        while solutionFound == 0:
            previousScore = score
            for i in range (0, iterations):
                newState = self.ChooseNewState(tmpSudoku, fixedSudoku, listOfBlocks, temperature)
                tmpSudoku = newState[0]
                scoreDiff = newState[1]
                score += scoreDiff
                result += [-score]
                if score == 0:
                    solutionFound = 1
                    break

            temperature *= decreaseFactor
            if score == 0:
                solutionFound = 1
                break
            if score >= previousScore:
                stuckCount += 1
            else:
                stuckCount = 0
            if stuckCount > 80:
                temperature += 2
        self.solution = tmpSudoku
        if printR == True:
            self.printSudoku(tmpSudoku)
        print("--- %s seconds ---" % (time.time() - start_time))
        plt.plot(result)
        plt.ylabel("Number of Error(s)")
        plt.xlabel("Number of Tries")
        plt.show()
        
start_time = time.time()

# Run the program
def main(argv):
    puzzle = Sudoku()
    path = ''
    for testCase in argv:
        # print(testCase)
        puzzle.load(testCase)
        # tracemalloc.start()
        puzzle.solve()
        # print("--- %s seconds ---" % (time.time() - start_time))
        # snapshot = tracemalloc.take_snapshot()
        # tracemalloc.stop()
        # display_top(snapshot)
        print('\n')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        main(["test_1.txt"])