"""
Multiplies two random matrices by multiprocess programming
"""

import multiprocessing
import random


class Multiplier(multiprocessing.Process):
    def __init__(self, ma1: list, ma2: list, ind=0, *args, **kwargs):
        self._ma1 = ma1
        self._ma2 = ma2
        self._ind = ind
        self._result = multiprocessing.Queue()
        super().__init__(*args, **kwargs)
        print(f"Process {self.name}: Matrix 1's chunk{self.ind}: {self._ma1}, Index: {self._ind}")

    def run(self) -> None:
        # Create the framework of result matrix
        res = [[False for y in range(len(self._ma2[0]))] for x in range(len(self._ma1))]
        # Multiplication
        for row in range(len(self._ma1)):
            for column in range(len(self._ma2[0])):
                temp = 0
                for j in range(len(self._ma2)):
                    temp += self._ma1[row][j] * self._ma2[j][column]
                res[row][column] = temp
        # Put the result matrix to the process's queue
        if len(res) != 0:
            self.result.put(res)
    
    @property
    def result(self):
        return self._result
    
    @property
    def ind(self):
        return self._ind


def get_numbers(m: int, t: str) -> int:
    """
    Takes the number of rows and columns of matrices from user
    :param m: Matrix indicator shown in input prompt
    :param t: Indicates the type of input, whether Row or Column
    :return: Returns the user's input
    :rtype: int
    """
    while True:
        if m == 1:
            u_in = input(f"Please insert the number of {t} of first matrix: ")
        else:
            u_in = input(f"Please insert the number of {t} of second matrix: ")
        if (u_in.isdecimal()) and (0 < int(u_in) < 10):
            return int(u_in)
        else:
            print("The input must be a positive integer less than 10!")
            continue


def matrices_creator() -> tuple:
    """
    Creates random matrices with user given dimensions
    :return: (matrix 1, matrix 2)
    :rtype: tuple
    """
    while True:
        x1 = get_numbers(1, "Rows")
        y1 = get_numbers(1, "Columns")
        x2 = get_numbers(2, "Rows")
        y2 = get_numbers(2, "Columns")
        if y1 != x2:
            print("To do multiplication, the number of first matrix's columns must be equal to the"
                  " second one's rows!")
            continue
        else:
            break
    # Creating random matrices
    ma1 = [[random.randint(1, 5) for y in range(y1)] for x in range(x1)]
    ma2 = [[random.randint(1, 5) for y in range(y2)] for x in range(x2)]
    return ma1, ma2


if __name__ == "__main__":
    m1, m2 = matrices_creator()
    print()
    print("Matrix 1:")
    for r1 in m1:
        print(r1)
    print()
    print("Matrix 2:")
    for r2 in m2:
        print(r2)
    print()

    # Set the number of processes to the number of first matrix's rows
    proc_num = len(m1)
    processes = []

    # Chunking the first matrix to do multiplication through different processes
    for i in range(proc_num):
        start = i
        end = i + 1
        processes.append(Multiplier(m1[start: end], m2, start, name=f"P{i}"))

    # Starting processes and wait for them to finish their job
    [p.start() for p in processes]
    [p.join() for p in processes]
    result = []
    # Combine the results of processes to make the result
    for p in processes:
        result.insert(p.ind, p.result.get())
    print()
    print("Result:")
    for r in result:
        print(r)
