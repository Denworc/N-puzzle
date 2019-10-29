from solv import *
import sys


def check_input(l):
    puzzle = []
    for line in l:
        new = line.split('#', 1)[0]
        new = ' '.join(new.split())
        if new:
            puzzle.append(new)
    if len(puzzle[0].split()) > 1:
        print("Error: There should be only size in first line")
        return False
    if int(puzzle[0]) < 3:
        print("Error: Size must be more then 2")
        return False
    if not puzzle[0].isnumeric():
        print("Error: There should be size in first line")
        return False
    if not len(puzzle) == int(puzzle[0]) + 1:
        print("Error: Wrong lines number")
        return False
    for line in puzzle[1:]:
        if not len(line.split()) == int(puzzle[0]):
            print("Error: Wrong number of elements")
            return False
        for n in line.split():
            if not n.isnumeric():
                print("Error: Only numbers are allowed")
                return False
    return puzzle


def get_res_puzzle(n):
    mat = [[0] * n for i in range(n)]
    st, m = 1, 0
    for v in range(n // 2):
        for i in range(n - m):
            if st < n * n:
                mat[v][i + v] = st
            st += 1
        for i in range(v + 1, n - v):
            if st < n * n:
                mat[i][-v - 1] = st
            st += 1
        for i in range(v + 1, n - v):
            if st < n * n:
                mat[-v - 1][-i - 1] = st
            st += 1
        for i in range(v + 1, n - (v + 1)):
            if st < n * n:
                mat[-i - 1][v] = st
            st += 1
        m += 2
    return mat


def get_puzzle(p):
    puzzle = [list(map(int, i.split())) for i in p[1:]]
    return puzzle


def check_elems(puzzle):
    sqr = len(puzzle) * len(puzzle)
    c = [j for i in puzzle for j in i]
    for line in puzzle:
        for elem in line:
            if elem >= sqr:
                print("Error: Each element should be less than N*N")
                sys.exit()
            if c.count(elem) > 1:
                print("Error: Identical elements")
                sys.exit()


def is_solvable(puzzle):
    n = len(puzzle)
    c = []
    st, m = 1, 0
    summ = 0
    for v in range(n // 2):
        for i in range(n - m):
            if puzzle[v][i + v] > 0:
                c.append(puzzle[v][i + v])
            st += 1
        for i in range(v + 1, n - v):
            if puzzle[i][-v - 1] > 0:
                c.append(puzzle[i][-v - 1])
            st += 1
        for i in range(v + 1, n - v):
            if puzzle[-v - 1][-i - 1] > 0:
                c.append(puzzle[-v - 1][-i - 1])
            st += 1
        for i in range(v + 1, n - (v + 1)):
            if puzzle[-i - 1][v] > 0:
                c.append(puzzle[-i - 1][v])
            st += 1
        m += 2
    c.append(puzzle[n // 2][n // 2])
    for i in range(n * n - 1):
        for elem in c[i+1:]:
            if c[i] > elem > 0:
                summ += 1
    if summ % 2 == 0:
        return True
    else:
        return False


def check_solvable(p):
    if not p:
        sys.exit()
    else:
        puzzle = get_puzzle(p)
        check_elems(puzzle)
        res = get_res_puzzle(int(p[0]))
        if is_solvable(puzzle):
            solv(puzzle, res)
        else:
            print("This puzzle is unsolvable")
            sys.exit()
