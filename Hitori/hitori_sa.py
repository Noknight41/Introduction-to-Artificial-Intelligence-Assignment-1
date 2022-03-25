import time
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt
import sys
from collections import Counter, deque


class Hitori:
    def __init__(self, path=None):
        self.dimension = 0
        self.array_grid = []
        self.solution = []
        self.current_black = []
        self.have_visit = []
        self.dup_pairs = []
        self.dup_lists = {}
        self.temp_arr = []
        self.rng = np.random.default_rng()
        if path is not None and str == type(path): self.load(path)

    def load(self, path):
        self.array_grid = np.loadtxt(path, dtype=int).flatten()
        length = len(self.array_grid)
        self.dimension = int(math.sqrt(length))
        if length != self.dimension * self.dimension:
            raise {}

    def __printGrid(self, grid):
        i = 0
        for element in grid:
            if i == self.dimension:
                print()
                i = 0
            print(element, end=' ')
            i = i + 1

    def printSolution(self):
        self.__printGrid(self.solution)

    def printInitialGrid(self):
        self.__printGrid(self.array_grid)

    def markDubs(self, pos):
        check_arr_hor = np.empty(11, dtype=object)
        check_arr_ver = np.empty(11, dtype=object)

        for i in range(11):
            check_arr_hor[i] = []
            check_arr_ver[i] = []

        for i in range(self.dimension):
            check_arr_hor[self.array_grid[pos * self.dimension + i]].append(pos * self.dimension + i)
            check_arr_ver[self.array_grid[i * self.dimension + pos]].append(i * self.dimension + pos)

        filter_crit = lambda x: len(x) > 1
        dub_list = list(filter(filter_crit, check_arr_hor)) + list(filter(filter_crit, check_arr_ver))

        return dub_list

    def __getDubsDict(self):
        dub_arr = []

        for i in range(self.dimension):
            dub_arr += self.markDubs(i)

        dub_list = sum(dub_arr, [])

        create_dict = lambda value: dict((v, 'u') for v in value)

        return [create_dict(sorted(Counter(dub_list))), dub_list]

    def checkDubs(self, pos):
        dub = 0
        check_arr_hor = np.full(11, 0)
        check_arr_ver = np.full(11, 0)

        for i in range(self.dimension):
            check_arr_hor[self.temp_arr[pos * self.dimension + i]] += 1

            check_arr_ver[self.temp_arr[i * self.dimension + pos]] += 1

        for i in range(1, 11):
            if 1 < check_arr_hor[i]:
                dub += check_arr_hor[i] - 1
            if 1 < check_arr_ver[i]:
                dub += check_arr_ver[i] - 1

        return dub

    def countTotalDub(self):
        dub_arr = 0

        for i in range(self.dimension):
            dub_arr += self.checkDubs(i)

        return np.sum(dub_arr)

    def __travelBlack(self, pos):
        result = False
        if self.have_visit[pos]:
            return result

        edge_check = lambda x: x < self.dimension or x > self.dimension * (
                self.dimension - 1) or 0 == x % self.dimension or 0 == (x + 1) % self.dimension
        edge_flag = False
        add_flag = False
        if edge_check(pos):
            edge_flag = True

        wait_line = deque()
        probe = [0, 0, 0, 0]

        current_check = pos
        for i in range(pos, len(self.current_black)):
            if self.have_visit[i]:
                continue
            else:
                wait_line.append(i)

            while len(wait_line):
                current_check = wait_line.pop()
                self.have_visit[pos] = True
                if (edge_flag and edge_check(current_check)) or pos == current_check:
                    result = True
                    break

                edge_flag = edge_check(current_check)

                if self.have_visit[current_check]:
                    result = False
                    break

                probe[0] = current_check - self.dimension - 1
                probe[1] = current_check - self.dimension + 1
                probe[2] = current_check + self.dimension - 1
                probe[3] = current_check + self.dimension + 1
                for ii in range(4):
                    if probe[ii] < self.dimension ** 2 and probe[ii] > 0 and 0 == self.temp_arr[probe[ii]]:
                        wait_line.append(probe[ii])

        return result

    def __checkIsland(self):
        """
        self.have_visit = np.full(self.dimension * self.dimension, False)

        for i in self.current_black:
            if self.__travelBlack(i):
                return True
        """
        whiteCell = []
        visited = []
        flag = False
        element = 0
        probe = [0, 0, 0, 0]
        wait_list = deque()
        for i in range(len(self.temp_arr)):
            if 0 != self.temp_arr[i]:
                whiteCell.append(i)
                if not flag:
                    flag = True
                    wait_list.append(i)
                    while len(wait_list):
                        element = wait_list.pop()
                        if element not in visited:
                            visited.append(element)
                            probe[0] = element - 1
                            probe[1] = element + 1
                            probe[2] = element - self.dimension
                            probe[3] = element + self.dimension
                            for ii in probe:
                                if ii >= 0 and ii < len(self.array_grid):
                                    if self.temp_arr[ii] != 0:
                                        wait_list.append(ii)

        return not len(visited) == len(whiteCell)

    def isIsland(self):
        return self.__checkIsland()

    def __checkNoContinueBlack(self):
        lenght = len(self.array_grid)
        bound_check = lambda x: x >= 0 and x < lenght
        check_element = lambda x : [x + 1, x - 1, x + self.dimension, x - self.dimension]
        crit = lambda x : bound_check(x) and 0 == self.temp_arr[x]
        for i in range(len(self.temp_arr)):
            if 0 == self.temp_arr[i]:
                if sum(map(crit ,check_element(i))):
                    return True
        return False

    def checkResult(self):
        return not (self.__checkIsland() or self.__checkNoContinueBlack())

    # Quick hard-code case detect and solve
    def initSolver(self, tempHitori):
        if 2 < self.dimension:
            corner_case = [0, self.dimension - 1, len(self.array_grid) - self.dimension,
                           len(self.array_grid) - 1]
            if (0 in self.dup_lists) and (1 in self.dup_lists) and (self.dimension in self.dup_lists):
                if self.array_grid[0] == self.array_grid[1] and self.array_grid[0] == self.array_grid[self.dimension]:
                    self.dup_lists[0] = 'b'
                    self.dup_lists[1] = 'w'
                    self.dup_lists[self.dimension] = 'w'
                    tempHitori[0] = 0
                    self.current_black.append(0)

            if self.dimension - 1 in self.dup_lists and self.dimension - 2 in self.dup_lists and 2 * self.dimension - 1 in self.dup_lists:
                if self.array_grid[self.dimension - 1] == self.array_grid[self.dimension - 2] and self.array_grid[self.dimension - 1] == self.array_grid[2 * self.dimension - 1]:
                    self.dup_lists[self.dimension - 1] = 'b'
                    self.dup_lists[self.dimension - 2] = 'w'
                    self.dup_lists[2 * self.dimension - 1] = 'w'
                    tempHitori[self.dimension - 1] = 0
                    self.current_black.append(self.dimension - 1)

            if corner_case[2] in self.dup_lists and corner_case[2] - self.dimension in self.dup_lists and corner_case[
                2] + 1 in self.dup_lists:
                if self.array_grid[corner_case[2]] == self.array_grid[corner_case[2] - self.dimension] and self.array_grid[corner_case[2]] == self.array_grid[corner_case[2] + 1]:
                    self.dup_lists[corner_case[2]] = 'b'
                    self.dup_lists[corner_case[2] - self.dimension] = 'w'
                    self.dup_lists[corner_case[2] + 1] = 'w'
                    tempHitori[corner_case[2]] = 0
                    self.current_black.append(corner_case[2])

            if corner_case[3] in self.dup_lists and corner_case[3] - 1 in self.dup_lists and corner_case[
                3] - self.dimension in self.dup_lists:
                if self.array_grid[corner_case[3]] == self.array_grid[corner_case[3] - 1] and self.array_grid[corner_case[3]] == self.array_grid[corner_case[3] - self.dimension]:
                    self.dup_lists[corner_case[3]] = 'b'
                    self.dup_lists[corner_case[3] - 1] = 'w'
                    self.dup_lists[corner_case[3] - self.dimension] = 'w'
                    tempHitori[corner_case[3]] = 0
                    self.current_black.append(corner_case[3])

            for i in self.dup_lists.keys():
                if 'w' == self.dup_lists[i]:
                    continue
                if (i + 1 in self.dup_lists) and (i - 1 in self.dup_lists):
                    if self.array_grid[i] == self.array_grid[i + 1] and self.array_grid[i] == self.array_grid[i - 1]:
                        tempHitori[i + 1] = tempHitori[i - 1] = 0
                        self.dup_lists[i + 1] = self.dup_lists[i - 1] = 'b'
                        self.current_black.append(i + 1)
                        self.current_black.append(i - 1)
                elif (i + self.dimension in self.dup_lists) and (i + self.dimension in self.dup_lists):
                    if self.array_grid[i] == self.array_grid[i + self.dimension] and self.array_grid[i] == self.array_grid[i - self.dimension]:
                        tempHitori[i + self.dimension] = tempHitori[i - self.dimension] = 0
                        self.dup_lists[i + self.dimension] = self.dup_lists[i - self.dimension] = 'b'
                        self.current_black.append(i + self.dimension)
                        self.current_black.append(i - self.dimension)

        return tempHitori

    def madeNewChange(self, old_score, temperature, keys):
        pos = keys[self.rng.integers(0, len(keys))]
        old_value = self.temp_arr[pos], self.dup_lists[pos]
        result = 0
        if self.rng.uniform(0, 1, None) < 0.5:
            if 'b' == self.dup_lists[pos] or 'u' == self.dup_lists[pos]:
                self.dup_lists[pos] = 'w'
                self.temp_arr[pos] = self.array_grid[pos]
            else:
                self.dup_lists[pos] = 'b'
                self.temp_arr[pos] = 0

        new_score = self.__scoreCalc()
        score_delta = new_score - old_score
        #if 0 < score_delta:
        pr = math.exp((-score_delta / temperature))
        if self.rng.uniform(0, 1, None) < pr:
            result = score_delta
        else:
            self.temp_arr[pos] = old_value[0]
            self.dup_lists[pos] = old_value[1]

        if 'b' == self.dup_lists[pos]:
            self.current_black.append(pos)

        return result

    def __scoreCalc(self):
        return self.countTotalDub()

    def fillInitState(self):
        for i in self.dup_lists.keys():
            if 'u' == self.dup_lists[i]:
                if self.rng.uniform(0, 1, None) < 0.5:
                    self.current_black.append(i)
                    self.dup_lists[i] = 'b'
                    self.temp_arr[i] = 0
                else:
                    self.dup_lists[i] = 'w'

    def solve(self):
        start_time = time.time()
        stuckCount = 0
        
        decrease_factor = .99
        iterations_max = 0

        self.current_black = []
        tmp = self.__getDubsDict()

        self.dup_pairs = tmp[1]
        self.dup_lists = tmp[0]
        temperature = len(self.dup_lists) * 100
        
        hold_arr = np.copy(self.array_grid)
        self.temp_arr = self.initSolver(hold_arr)
        
        self.old_dub_lists = self.dup_lists
        
        tmp = self.__getDubsDict()

        self.dup_pairs = tmp[1]
        self.dup_lists = tmp[0]
        
        old_score = score = self.__scoreCalc()
        
        previous_score = 0
        is_solve = (not score) and self.checkResult()
        
        result = []
        counting = 0
        iterations_max = len(self.dup_lists)
        keys = [*self.dup_lists]
        while not is_solve:
            previous_score = score
            for i in range(iterations_max):
                counting += 1
                score += self.madeNewChange(score, temperature, keys)
                result.append(score)
                if 0 == score:
                    if self.checkResult():
                        is_solve = True
                        break

            temperature *= decrease_factor
            if 0 == score:
                if self.checkResult():
                    is_solve = True
            elif score >= previous_score:
                stuckCount += 1
                if stuckCount > 10:
                    temperature += 10
                    
            else:
                stuckCount = 0
            self.current_black = []
        print("--- %s seconds ---" % (time.time() - start_time))
        self.solution = np.copy(self.temp_arr)
        plt.plot(result)
        plt.ylabel("Number of Error(s)")
        plt.xlabel("Number of Tries")
        plt.show()


def main(argv):
    hitori = Hitori()
    for testCase in argv:
        hitori.load(testCase)
        hitori.solve()
        hitori.printSolution()


if __name__ == '__main__':
    # main(sys.argv[1:])
    main(["test1.txt"])


