import random
import numpy as np
import math 
from random import choice
import statistics 
import matplotlib.pyplot as plt

class Sudoku:    
    def __init__(self):
        pass
    
    # Load Sudoku from txt file 
    def load(self, path):
        with open(path, "r") as f:
            val = np.loadtxt(f).astype(int)
            self.n = int(math.sqrt(len(val)))
            self.m = int(math.sqrt(self.n))
            self.data = val.reshape((self.m * self.m, self.m * self.m))
        
    # Print the Sudoku
    def printSudoku(self, data):
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


    def ChooseNewState (self, currentSudoku, fixedSudoku, listOfBlocks, sigma):
        proposal = self.ProposedState(currentSudoku, fixedSudoku, listOfBlocks)
        newSudoku = proposal[0]
        boxesToCheck = proposal[1]
        
        # Check before/after value
        curVal = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1], currentSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0], boxesToCheck[1][1], currentSudoku)
        newVal = self.CalculateNumberOfErrorsRowColumn(boxesToCheck[0][0], boxesToCheck[0][1], newSudoku) + self.CalculateNumberOfErrorsRowColumn(boxesToCheck[1][0], boxesToCheck[1][1], newSudoku)
        
        costDifference = newVal - curVal
        rho = math.exp( -costDifference / sigma)
        if(np.random.uniform(1, 0, 1) < rho):
            return([newSudoku, costDifference])
        return([currentSudoku, 0])


    def ChooseNumberOfIterations(self, fixed_sudoku):
        numberOfIterations = 0
        for i in range (0, self.m ** 2):
            for j in range (0, self.m ** 2):
                if fixed_sudoku[i,j] != 0:
                    numberOfIterations += 1
        return numberOfIterations

    # Calculate Initial Sigma
    def CalculateInitialSigma(self, sudoku, fixedSudoku, listOfBlocks):
        listOfDifferences = []
        tmpSudoku = sudoku
        for i in range(1, self.m ** 2 + 1):
            tmpSudoku = self.ProposedState(tmpSudoku, fixedSudoku, listOfBlocks)[0]
            listOfDifferences.append(self.CalculateNumberOfErrors(tmpSudoku))
        return statistics.pstdev(listOfDifferences)

    # Solve the sudoku
    def solve(self):
        f = open("result.txt", "a")
        result = []
        solutionFound = 0
        decreaseFactor = 0.99
        stuckCount = 0
        fixedSudoku = np.copy(self.data)
        self.printSudoku(self.data)
        
        # Fixed Value and Assign Random Value to Sudoku
        fixedSudoku = self.FixSudokuValues(fixedSudoku)
        listOfBlocks = self.CreateListofBlocks()
        tmpSudoku = self.RandomlyFillBlocks(self.data, listOfBlocks)
        
        # Sigma + Score + Iterations
        sigma = self.CalculateInitialSigma(self.data, fixedSudoku, listOfBlocks)
        score = self.CalculateNumberOfErrors(tmpSudoku)
        iterations = self.ChooseNumberOfIterations(fixedSudoku)

        while solutionFound == 0:
            previousScore = score
            for i in range (0, iterations):
                newState = self.ChooseNewState(tmpSudoku, fixedSudoku, listOfBlocks, sigma)
                tmpSudoku = newState[0]
                scoreDiff = newState[1]
                score += scoreDiff
                result += [score]
                f.write(str(score) + '\n')
                if score == 0:
                    solutionFound = 1
                    break

            sigma *= decreaseFactor
            if score == 0:
                solutionFound = 1
                break
            if score >= previousScore:
                stuckCount += 1
            else:
                stuckCount = 0
            if (stuckCount > 80):
                sigma += 2
        f.close()
        self.solution = tmpSudoku
        self.printSudoku(tmpSudoku)
        plt.plot(result)
        plt.ylabel("Number of Error(s)")
        plt.xlabel("Number of Tries")
        plt.show()
        


sudoku = Sudoku()
sudoku.load("test_3.txt")
sudoku.solve()