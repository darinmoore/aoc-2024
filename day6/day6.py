#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 6
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from copy import deepcopy

import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
        """,
        41
    ),
]

SAMPLE_CASES2 = [
    (
        """
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
        """,
        6
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(
        Path(infile).read_text(), strip=strip, blank_lines=blank_lines
    )

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = text.strip("\n").split("\n")
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution
def find_guard(lines):
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j]== "^":
                return (i,j)
    return -1

def is_loop(lines):
    x, y = find_guard(lines)

    curr_dir = 0 # start going up
    delta_x, delta_y = DIRECTIONS[curr_dir] 
    
    ans = 0
    i = 0
    while i < 10000:
        new_x = x + delta_x
        new_y = y + delta_y

        if not (0 <= new_x < len(lines) and 0 <= new_y < len(lines[0])):
            return False
        elif lines[new_x][new_y] == '#':
            curr_dir = (curr_dir + 1) % 4
        else:
            x = new_x
            y = new_y
        delta_x, delta_y = DIRECTIONS[curr_dir]
        i += 1

    return True

DIRECTIONS = [
    (-1, 0), # UP 
    (0, 1),  # RIGHT
    (1, 0),  # DOWN 
    (0, -1)  # LEFT
]
def solve2(lines: Lines) -> int:
    """Solve the problem."""
    # first pop seen to get list of possible boulder spots
    x, y = find_guard(lines)

    curr_dir = 0 # start going up
    delta_x, delta_y = DIRECTIONS[curr_dir] 
    
    ans = 0
    seen = {(x,y)}
    while True:
        new_x = x + delta_x
        new_y = y + delta_y

        if not (0 <= new_x < len(lines) and 0 <= new_y < len(lines[0])):
            break
        elif lines[new_x][new_y] == '#':
            curr_dir = (curr_dir + 1) % 4
        else:
            x = new_x
            y = new_y
            seen.add((x,y))
        delta_x, delta_y = DIRECTIONS[curr_dir]

    seen.remove(find_guard(lines)) # starting pos cannot be boulder
    for boulder in seen:
        copy_lines = deepcopy(lines)
        boulder_x, boulder_y = boulder
        line_str = copy_lines[boulder_x]
        copy_lines[boulder_x] = line_str[:boulder_y] + '#' + line_str[boulder_y+1:]
        if is_loop(copy_lines):
            ans += 1

    return ans

def solve(lines: Lines) -> int:
    """Solve the problem."""
    x,y = find_guard(lines)
    seen = {(x,y)}
    curr_dir = 0 # start going up
    delta_x, delta_y = DIRECTIONS[curr_dir] 
    while True:
        new_x = x + delta_x
        new_y = y + delta_y

        if not (0 <= new_x < len(lines) and 0 <= new_y < len(lines[0])):
            break
        elif lines[new_x][new_y] == '#':
            curr_dir = (curr_dir + 1) % 4
        else:
            x = new_x
            y = new_y
            seen.add((x,y))
        delta_x, delta_y = DIRECTIONS[curr_dir]

    return len(seen)


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 5242
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == -1
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
