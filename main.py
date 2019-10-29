#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import os
import random
from PyInquirer import Validator, ValidationError

from check import *


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def change_pazzle(res):
    freeY, freeX = get_zero(res)
    size = len(res)

    i = random.randint(1, 4)
    if i == 1:
        if freeY + 1 < size:
            first = copy.deepcopy(res)
            first[freeY + 1][freeX], first[freeY][freeX] = first[freeY][freeX], first[freeY + 1][freeX]
            if first != res:
                return first
    elif i == 2:
        if freeY - 1 > -1:
            second = copy.deepcopy(res)
            second[freeY - 1][freeX], second[freeY][freeX] = second[freeY][freeX], second[freeY - 1][freeX]
            if second != res:
                return second
    elif i == 3:
        if freeX + 1 < size:
            third = copy.deepcopy(res)
            third[freeY][freeX + 1], third[freeY][freeX] = third[freeY][freeX], third[freeY][freeX + 1]
            if third != res:
                return third
    else:
        if freeX - 1 > -1:
            fourth = copy.deepcopy(res)
            fourth[freeY][freeX - 1], fourth[freeY][freeX] = fourth[freeY][freeX], fourth[freeY][freeX - 1]
            if fourth != res:
                return fourth
    return res


def get_gen():
    questions = [
        {
            'type': 'input',
            'name': 'size',
            'message': 'N-Puzzle size?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
    ]
    try:
        answers = prompt(questions)
    except:
        print("Looks like you closed the program.")
        sys.exit()
    if answers['size'] > 6 or answers['size'] < 2:
        print("Size must be lower then 7 and more then 2")
        sys.exit()
    else:
        size = answers['size']
    questions = [
        {
            'type': 'input',
            'name': 'complexity',
            'message': 'Сomplexity?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
    ]
    try:
        answers = prompt(questions)
    except:
        print("Looks like you closed the program.")
        sys.exit()
    if answers['complexity'] > 500 or answers['complexity'] < 5:
        print("Size must be lower then 500 and more then 5")
        sys.exit()
    else:
        complexity = answers['complexity']
    res = get_res_puzzle(int(size))
    buff = copy.deepcopy(res)
    for i in range(complexity):
        res = change_pazzle(res)
    solv(res, buff)


def get_file():
    questions = [
        {
            'type': 'input',
            'name': 'file',
            'message': 'Write file name',
            'default': 'test.txt'
        },
    ]
    try:
        answers = prompt(questions)
    except:
        print("Looks like you closed the program.")
        sys.exit()

    if os.path.exists("test/" + answers['file']):
        f = open("test/" + answers['file'], 'r')
        l = [line.strip() for line in f]
        f.close()
        check_solvable(check_input(l))
    else:
        print("File not found, try again")
        get_file()


def get_manual():
    questions = [
        {
            'type': 'input',
            'name': 'size',
            'message': 'N-Puzzle size?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
    ]
    try:
        answers = prompt(questions)
    except:
        print("Looks like you closed the program.")
        sys.exit()
    if answers['size'] > 6 or answers['size'] < 2:
        print("Size must be lower then 7 and more then 2")
        sys.exit()
    else:
        size = answers['size']
    buff = [str(size)]
    for i in range(size):
        questions = [
            {
                'type': 'input',
                'name': 'line',
                'message': 'Add new line to the puzzle:',
                'default': ''
            },
        ]
        try:
            answers = prompt(questions)
        except:
            print("Looks like you closed the program.")
            sys.exit()
        buff.append(answers['line'] + "")
    check_solvable(check_input(buff))


def input_type():
    questions = [
        {
            'type': 'list',
            'message': 'Select input type',
            'name': 'input',
            'choices': [
                Separator('= Inputs ='),
                {
                    'name': 'File'
                },
                {
                    'name': 'Manual'
                },
                {
                    'name': 'Generator'
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
    if answers['input'] == 'File':
        get_file()
    elif answers['input'] == 'Manual':
        get_manual()
    else:
        get_gen()


def n_puzzle():
    input_type()


if __name__ == '__main__':
    n_puzzle()
