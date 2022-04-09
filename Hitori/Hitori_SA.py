import time
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt
import sys
from collections import Counter, deque

import tracemalloc
import linecache
import os

a = 0

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
    print("Total allocated size: %.1f B" % total)
    print(total)

class Hitori:
    def __init__(self, path=None):
        self.old_dub_lists = []
        self.dimension = 0
        self.array_grid = []
        self.solution = []
        self.have_visit = []
        self.dup_pairs = []
        self.dup_lists = {}
        self.temp_arr = []
        self.rng = np.random.default_rng()
        if path is not None and str == type(path):
            self.load(path)

    def load(self, path):
        with open('demo_step_by_step_sa.txt','w') as f: pass
        self.array_grid = np.loadtxt(path, dtype=int).flatten()
        length = len(self.array_grid)
        self.dimension = int(math.sqrt(length))
        if length != self.dimension * self.dimension:
            raise RuntimeError("Incorrect dimension!")
        self.printInitialGrid()

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

    def __markDubs(self, pos):
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
            dub_arr += self.__markDubs(i)

        dub_list = sum(dub_arr, [])

        create_dict = lambda value: dict((v, 'u') for v in value)

        return [create_dict(sorted(Counter(dub_list))), dub_list]

    def __checkDubs(self, pos, check_arr_hor, check_arr_ver) -> int:
        dub = 0

        for i in range(self.dimension):
            check_arr_hor[self.temp_arr[pos * self.dimension + i]] += 1

            check_arr_ver[self.temp_arr[i * self.dimension + pos]] += 1

        for i in range(1, 11):
            if 1 < check_arr_hor[i]:
                dub += check_arr_hor[i] - 1
            if 1 < check_arr_ver[i]:
                dub += check_arr_ver[i] - 1

            check_arr_hor[i] = check_arr_ver[i] = 0

        return dub

    def __countTotalDub(self) -> int:
        dub_arr = 0

        check_arr_hor = np.full(11, 0)
        check_arr_ver = np.full(11, 0)

        for i in range(self.dimension):
            dub_arr += self.__checkDubs(i, check_arr_hor, check_arr_ver)

        return np.sum(dub_arr)

    def __checkIsland(self):
        white_cell = []
        visited = []
        flag = False
        element = 0
        probe = [0, 0, 0, 0]
        wait_list = deque()
        length = len(self.temp_arr)
        for i in range(length):
            if 0 != self.temp_arr[i]:
                white_cell.append(i)
                if not flag:
                    flag = True
                    wait_list.append(i)
                    while len(wait_list):
                        element = wait_list.pop()
                        if element not in visited:
                            visited.append(element)
                            probe[0] = element - 1
                            if int(probe[0] / self.dimension) != int(element / self.dimension):
                                probe[0] = element
                            probe[1] = element + 1
                            if int(probe[1] / self.dimension) != int(element / self.dimension):
                                probe[1] = element
                            probe[2] = element - self.dimension
                            probe[3] = element + self.dimension
                            for ii in probe:
                                if 0 <= ii < length:
                                    if 0 != self.temp_arr[ii]:
                                        wait_list.append(ii)

        return len(visited) != len(white_cell)

    def __checkNoContinueBlack(self):
        length = len(self.array_grid)
        bound_check = lambda x: 0 <= x < length
        row_check = lambda x, base: [x] if int(x / self.dimension) == int(base / self.dimension) else []
        check_element = lambda x: row_check(x + 1, x) + row_check(x - 1, x) + [x + self.dimension, x - self.dimension]
        crit = lambda x: bound_check(x) and 0 == self.temp_arr[x]
        for i in self.old_dub_lists.keys():
            if 0 == self.temp_arr[i]:
                if sum(map(crit, check_element(i))):
                    return True
        return False

    def __checkResult(self):
        return not (self.__checkIsland() or self.__checkNoContinueBlack())

    # Quick hard-code case detect and solve
    def __initSolver(self, temp_hitori) -> list:
        if 2 < self.dimension:
            corner_case = [0, self.dimension - 1, len(self.array_grid) - self.dimension,
                           len(self.array_grid) - 1]
            if (0 in self.dup_lists) and (1 in self.dup_lists) and (self.dimension in self.dup_lists):
                if self.array_grid[0] == self.array_grid[1] and self.array_grid[0] == self.array_grid[self.dimension]:
                    self.dup_lists[0] = 'b'
                    self.dup_lists[1] = 'w'
                    self.dup_lists[self.dimension] = 'w'
                    temp_hitori[0] = 0

            if self.dimension - 1 in self.dup_lists and self.dimension - 2 in self.dup_lists and 2 * self.dimension - 1 in self.dup_lists:
                if self.array_grid[self.dimension - 1] == self.array_grid[self.dimension - 2] and self.array_grid[
                    self.dimension - 1] == self.array_grid[2 * self.dimension - 1]:
                    self.dup_lists[self.dimension - 1] = 'b'
                    self.dup_lists[self.dimension - 2] = self.dup_lists[2 * self.dimension - 1] = 'w'
                    temp_hitori[self.dimension - 1] = 0

            if corner_case[2] in self.dup_lists and corner_case[2] - self.dimension in self.dup_lists and corner_case[
                2] + 1 in self.dup_lists:
                if self.array_grid[corner_case[2]] == self.array_grid[corner_case[2] - self.dimension] and \
                        self.array_grid[corner_case[2]] == self.array_grid[corner_case[2] + 1]:
                    self.dup_lists[corner_case[2]] = 'b'
                    self.dup_lists[corner_case[2] - self.dimension] = self.dup_lists[corner_case[2] + 1] = 'w'
                    temp_hitori[corner_case[2]] = 0

            if corner_case[3] in self.dup_lists and corner_case[3] - 1 in self.dup_lists and corner_case[
                3] - self.dimension in self.dup_lists:
                if self.array_grid[corner_case[3]] == self.array_grid[corner_case[3] - 1] and self.array_grid[
                    corner_case[3]] == self.array_grid[corner_case[3] - self.dimension]:
                    self.dup_lists[corner_case[3]] = 'b'
                    self.dup_lists[corner_case[3] - 1] = 'w'
                    self.dup_lists[corner_case[3] - self.dimension] = 'w'
                    temp_hitori[corner_case[3]] = 0

            for i in self.dup_lists.keys():
                if 'w' == self.dup_lists[i]:
                    continue
                if (i + 1 in self.dup_lists) and (i - 1 in self.dup_lists):
                    if self.array_grid[i] == self.array_grid[i + 1] and self.array_grid[i] == self.array_grid[i - 1]:
                        temp_hitori[i + 1] = temp_hitori[i - 1] = 0
                        self.dup_lists[i + 1] = self.dup_lists[i - 1] = 'b'
                elif (i + self.dimension in self.dup_lists) and (i + self.dimension in self.dup_lists):
                    if self.array_grid[i] == self.array_grid[i + self.dimension] and self.array_grid[i] == \
                            self.array_grid[i - self.dimension]:
                        temp_hitori[i + self.dimension] = temp_hitori[i - self.dimension] = 0
                        self.dup_lists[i + self.dimension] = self.dup_lists[i - self.dimension] = 'b'

        return temp_hitori

    def __madeNewChange(self, old_score, temperature, keys) -> int:
        pos = keys[self.rng.integers(0, len(keys))]
        old_value = self.temp_arr[pos], self.dup_lists[pos]
        result = 0
        # if self.rng.uniform(0, 1, None) < 0.5:
        if 'b' == self.dup_lists[pos]:
            self.dup_lists[pos] = 'w'
            self.temp_arr[pos] = self.array_grid[pos]
        else:
            self.dup_lists[pos] = 'b'
            self.temp_arr[pos] = 0

        new_score = self.__scoreCalc()
        score_delta = new_score - old_score

        pr = math.exp((- score_delta / temperature))
        if score_delta < 0 or self.rng.uniform(0, 1, None) < pr:
            result = score_delta
        else:
            self.temp_arr[pos] = old_value[0]
            self.dup_lists[pos] = old_value[1]

        return result

    def __scoreCalc(self) -> int:
        return self.__countTotalDub()

    def fillInitState(self):
        for i in self.dup_lists.keys():
            if 'u' == self.dup_lists[i]:
                if self.rng.uniform(0, 1, None) < 0.5:
                    self.dup_lists[i] = 'b'
                    self.temp_arr[i] = 0
                else:
                    self.dup_lists[i] = 'w'
    
    def demoWritePuzzle(self, grid):
        with open('demo_step_by_step_sa.txt', 'a') as f:
            i = 0
            line = ""
            global a
            a += 1
            f.writelines("Step " + str(a) + '\n')
            for element in grid:
                line += str(element) + " "
                i = i + 1
                if i == self.dimension:
                    f.writelines(line + '\n')
                    line = ""
                    i = 0
            f.writelines('\n\n')

    def solve(self):
        start_time = time.time()
        stuck_count = 0

        decrease_factor = .99

        tmp = self.__getDubsDict()

        self.dup_pairs = tmp[1]
        self.dup_lists = tmp[0]
        temperature = len(self.dup_lists) * 100

        # self.temp_arr = np.copy(self.array_grid)
        # hold_arr = np.copy(self.array_grid)
        self.temp_arr = self.__initSolver(np.copy(self.array_grid))

        self.old_dub_lists = self.dup_lists

        tmp = self.__getDubsDict()

        self.dup_pairs = tmp[1]
        self.dup_lists = tmp[0]

        previous_score = score = self.__scoreCalc()

        is_solve = (not score) and self.__checkResult()

        result = []
        counting = 0
        iterations_max = len(self.dup_lists)
        keys = [*self.dup_lists]
        while not is_solve:
            previous_score = score
            for i in range(iterations_max):
                counting += 1
                score += self.__madeNewChange(score, temperature, keys)
                self.demoWritePuzzle(self.temp_arr)
                result.append(score)
                if 0 == score:
                    if self.__checkResult():
                        is_solve = True
                        break

            temperature *= decrease_factor

            if 0 == score and not is_solve:
                if self.__checkResult():
                    is_solve = True
            elif score >= previous_score:
                stuck_count += 1
                if stuck_count > 10:
                    if temperature < self.dimension * 2:
                        temperature += 10
                    temperature *= 1.1
            else:
                stuck_count = 0

        self.solution = np.copy(self.temp_arr)
        # print(len(result))
        # print((time.time() - start_time))
        print("\n--- %s seconds ---" % (time.time() - start_time))
        # plt.plot(result)
        # plt.ylabel("Number of Error(s)")
        # plt.xlabel("Number of Tries")
        # plt.show()


def main(argv):
    hitori = Hitori()
    path = ''
    for testCase in argv:
        # print(testCase)
        # hitori.load(path + testCase)
        hitori.load(testCase)
        # tracemalloc.start()
        hitori.solve()
        hitori.printSolution()
        # tracemalloc.stop()
        # snapshot = tracemalloc.take_snapshot()
        # display_top(snapshot)
        print('\n')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        main(["test_1.txt"])
