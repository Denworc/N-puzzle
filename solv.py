from __future__ import print_function, unicode_literals

import sys
import copy
from pprint import pprint
from queue import PriorityQueue


from PyInquirer import prompt, Separator


class Container:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.heuristic = 0
        self.step = 0
        self.priority = self.step + self.heuristic
        self.parent = ""

    def update(self, step, heuristic, greed):
        self.heuristic = heuristic
        self.step = step
        if greed:
            self.priority = 0 + self.heuristic
        else:
            self.priority = self.step + self.heuristic

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return self.puzzle


def get_zero(current):
    return next((y, x) for y, l in enumerate(current) for x, val in enumerate(l) if val == 0)


def get_coord(current, elem):
    return next((y, x) for y, l in enumerate(current) for x, val in enumerate(l) if val == elem)


def get_children(current):
    children = []
    freeY, freeX = get_zero(current.puzzle)
    size = len(current.puzzle[0])

    if freeY + 1 < size:
        first = copy.deepcopy(current.puzzle)
        first[freeY + 1][freeX], first[freeY][freeX] = first[freeY][freeX], first[freeY + 1][freeX]
        if first != current.puzzle:
            children.append(Container(first))
    if freeY - 1 > -1:
        second = copy.deepcopy(current.puzzle)
        second[freeY - 1][freeX], second[freeY][freeX] = second[freeY][freeX], second[freeY - 1][freeX]
        if second != current.puzzle:
            children.append(Container(second))
    if freeX + 1 < size:
        third = copy.deepcopy(current.puzzle)
        third[freeY][freeX + 1], third[freeY][freeX] = third[freeY][freeX], third[freeY][freeX + 1]
        if third != current.puzzle:
            children.append(Container(third))
    if freeX - 1 > -1:
        fourth = copy.deepcopy(current.puzzle)
        fourth[freeY][freeX - 1], fourth[freeY][freeX] = fourth[freeY][freeX], fourth[freeY][freeX - 1]
        if fourth != current.puzzle:
            children.append(Container(fourth))
    for child in children:
        child.parent = current
    return children


def misplaced(res, next):
    l = len(next[0]) ** 2
    sum = 0
    for i in range(1, l):
        if not (get_coord(next, i) == get_coord(res, i)):
            sum += 1
    return sum


def manhattan(res, next):
    l = len(next[0]) ** 2
    sum = 0
    for i in range(1, l):
        y, x = get_coord(next, i)
        resY, resX = get_coord(res, i)
        dx = abs(x - resX)
        dy = abs(y - resY)
        sum += dx + dy
    return sum


def linear(res, next):
    h = manhattan(res, next)
    line = 0
    l = len(next) ** 2
    for i in range(1, l):
        y, x = get_coord(next, i)
        resY, resX = get_coord(res, i)
        if not (bool(y == resY) == bool(x == resX)):
            line += 1
    return h + line


def heuristic(res, next, h):
    if h == 1:
        return misplaced(res, next)
    elif h == 2:
        return manhattan(res, next)
    elif h == 3:
        return linear(res, next)
    elif h == 4:
        return manhattan(res, next)
    else:
        return 0


def get_moves(start, current):
    path = [current]
    p = current.parent
    while p.puzzle != start.puzzle:
        path.append(p)
        p = p.parent
    path.append(start)
    return list(reversed(path))


def is_in(puzzle, buff):
    for elem in buff:
        if puzzle.puzzle == elem.puzzle:
            if puzzle.priority >= elem.priority:
                return False
    return True


def a_star(puzzle, res, h):
    open = PriorityQueue()
    start = Container(puzzle)
    start.update(0, heuristic(res, start.puzzle, h), False)
    open.put(start)
    summ = 0
    cost_so_far = {}
    cost_so_far[start] = start.priority
    while not open.empty():
        current = open.get()
        summ += 1
        if current.puzzle == res:
            for move in get_moves(start, current):
                print("Move №", move.step)
                for elem in move.puzzle:
                    collect = []
                    for i in elem:
                        collect.append(i)
                    print(collect)
                print("\n")
            print("Number of moves from initial state to solution:", current.step)
            print("Complexity in time:", summ)
            print("Complexity in size:", len(cost_so_far))
            break
        children = get_children(current)
        for next in children:
            new_cost = current.step + 1
            next.update(new_cost, heuristic(res, next.puzzle, h), False if not h == 4 else True)
            if is_in(next, cost_so_far):
                cost_so_far[next] = next.priority
                open.put(next)


def solv(puzzle, res):
    if puzzle == res:
        print("Puzzle is already solved")
        sys.exit()
    questions = [
        {
            'type': 'list',
            'message': 'Select heuristic',
            'name': 'heuristic',
            'choices': [
                Separator('= Inputs ='),
                {
                    'name': 'Misplaced'
                },
                {
                    'name': 'Manhattan'
                },
                {
                    'name': 'Linear'
                },
                {
                    'name': 'Greedy'
                },
                {
                    'name': 'Uniform_cost'
                },
            ],
            'validate': lambda answer: 'You must choose at least one input type.' \
                if len(answer) == 0 else True
        }
    ]
    try:
        answers = prompt(questions)
    except:
        print("Looks like you closed the program.")
        sys.exit()
    if answers['heuristic'] == 'Misplaced':
        a_star(puzzle, res, 1)
    elif answers['heuristic'] == 'Manhattan':
        a_star(puzzle, res, 2)
    elif answers['heuristic'] == 'Linear':
        a_star(puzzle, res, 3)
    elif answers['heuristic'] == 'Greedy':
        a_star(puzzle, res, 4)
    else:
        a_star(puzzle, res, 5)
