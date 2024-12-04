#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 2
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
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        """,
        2
    ),
]

SAMPLE_CASES2 = [
    (
        """
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        """,
        4
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
def parse_lines(lines):
    new_lines = []
    for line in lines:
        new_line = line.strip().split()
        new_line = [int(item) for item in new_line]
        new_lines.append(new_line)
    return new_lines

def is_safe(line):
    deltas = get_deltas_list(line)
    is_increasing = all([delta in {1, 2, 3} for delta in deltas])
    is_decreasing = all([delta in {-1,-2,-3} for delta in deltas])

    return is_increasing or is_decreasing

def is_safe_new(line):
    deltas = get_deltas_list(line)
    is_line_safe = is_safe(line)
    if not is_line_safe:
        # find first delta that breaks it, then retry by removing one of three elements
        # involved in that delta computation
        if deltas[0] > 0:
            for i in range(len(deltas)):
                delta = deltas[i]
                if delta not in {1,2,3}:
                    return (
                        is_safe(line[:i-1] + line[i:]) or 
                        is_safe(line[:i] + line[i+1:]) or 
                        is_safe(line[:i+1] + line[i+2:])
                    )
        elif deltas[0] < 0:
            for i in range(len(deltas)):
                delta = deltas[i]
                if delta not in {-1,-2,-3}:
                    return (
                        is_safe(line[:i-1] + line[i:]) or 
                        is_safe(line[:i] + line[i+1:]) or 
                        is_safe(line[:i+1] + line[i+2:])
                    )
        elif deltas[0] == 0:
            return is_safe(line[1:])
        return False
    return True

def get_deltas_list(line):
    deltas = []
    for i in range(len(line) - 1):
        deltas.append(line[i+1] - line[i])
    return deltas

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    lines = parse_lines(lines)
    return sum([1 for line in lines if is_safe_new(line)])

def solve(lines: Lines) -> int:
    """Solve the problem."""
    lines = parse_lines(lines)
    return sum([1 for line in lines if is_safe(line)])


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
    assert result == 524
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
    assert result == 569
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
