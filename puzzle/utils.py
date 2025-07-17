import random

def read_puzzle_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    puzzle = []
    for line in lines:
        puzzle.extend([int(x) for x in line.strip().split()])
    return tuple(puzzle)