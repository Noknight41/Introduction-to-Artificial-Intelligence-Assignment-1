# Introduction to Artificial Intelligence - Assignment 1

## Problem Summary

[Summary](./Report/Summary.pdf)


## Installation

To get started with the Sudoku Solver, clone the Repository:
   ```sh
   git clone https://github.com/Noknight41/Introduction-to-Artificial-Intelligence-Assignment-1
   ```

##  Sudoku Solver Project

Welcome to the Sudoku Solver Project! This project aims to provide a comprehensive solution for solving Sudoku puzzles efficiently and accurately. 

Sudoku, a popular number puzzle game, involves filling a 9x9 grid so that each column, each row, and each of the nine 3x3 grids contain all of the digits from 1 to 9. Our project offers a programmatic way to solve these puzzles, making it a handy tool for enthusiasts and developers alike.

## Solving Sudoku

### **Using Depth-First Search Algorithm**:

```sh
cd Sudoku
python sudoku_DFS.py
```

Default, the program will run [this testcase file](./Sudoku/test_1.txt)

To run the solver with a specified puzzle file:

```sh
python sudoku_DFS.py [test_case_file]
```

Example:


```sh
python sudoku_DFS.py test_2.txt
```

### **Using Simulated Annealing Search Algorithm**:

```sh
python sudoku_SA.py
```

Same behavior as DFS file, using sudoku_SA.py file instead of sudoku_DFS.py file

## Hitori Solver Project

Welcome to the Hitori Solver Project! This project aims to provide a comprehensive solution for solving Hitori puzzles efficiently and accurately. 

Hitori, a popular logic puzzle game, involves filling a grid with numbers such that no number appears more than once in any row or column, and all unshaded cells are connected horizontally or vertically in a single group. Our project offers a programmatic way to solve these puzzles, making it a handy tool for enthusiasts and developers alike.

## Solving Hitori

### **Using Depth-First Search Algorithm**:

```sh
cd Hitori
python Hitori_DFS.py
```

Default, the program will run [this testcase file](./Hitori/test_1.txt)

To run the solver with a specified puzzle file:

```sh
python Hitori_DFS.py [test_case_file]
```

Example:

```sh
python Hitori_DFS.py test_2.txt
```

### **Using Simulated Annealing Search Algorithm**:

```sh
python Hitori_SA.py
```

Same behavior as DFS file, using Hitori_SA.py file instead of Hitori_DFS.py file

---

Happy solving!
