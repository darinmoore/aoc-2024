#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 4
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """,
        18
    ),
]

SAMPLE_CASES2 = [
    (
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """,
        9
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
def get_neighbors(pos, grid):
    x,y = pos
    neighbors = []
    for deltaX in [-1, 0, 1]:
        for deltaY in [-1, 0, 1]:
            if deltaX or deltaY:
                new_x = x + deltaX 
                new_y = y + deltaY
                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                    neighbors.append((new_x, new_y))
    return neighbors

BLOCKS = [
    [(0,0), (0,1), (0, 2), (0, 3)],
    [(0,0), (1,0), (2, 0), (3, 0)],
    [(0, 0), (1, 1), (2, 2), (3, 3)],
    [(0, 3), (1, 2), (2, 1), (3, 0)]
]

X_BLOCKS = [
    [(-1,-1), (-1,1), (0,0), (1,-1), (1,1)]
]
def get_valid_words(x, y, grid, target_words, pattern):
    valid_words = 0
    for block in pattern:
        word = ''
        for deltaX, deltaY in block:
            new_x = deltaX + x
            new_y = deltaY + y
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                word += grid[new_x][new_y]
        if word in target_words:
            valid_words += 1
    return valid_words


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid = [list(line) for line in lines]
    ans = 0
    target_words = {'MMASS', 'SSAMM', 'MSAMS', 'SMASM'}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ans += get_valid_words(i, j, grid, target_words, X_BLOCKS)
    return ans

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = [list(line) for line in lines]
    ans = 0
    target_words = {'XMAS', 'SAMX'}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ans += get_valid_words(i, j, grid, target_words, BLOCKS)
    return ans


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
    assert result == 2464
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
