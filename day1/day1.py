#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 1
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
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
        """,
        11
    ),
]

SAMPLE_CASES2 = [
    (
        """
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
        """,
        31
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
def parse_lists(lines):
    list1 = []
    list2 = []
    for line in lines:
        item1, item2 = line.strip().split()
        list1.append(int(item1))
        list2.append(int(item2))
    return list1, list2

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    left_list, right_list = parse_lists(lines)
    
    num_occurs = defaultdict(int)
    for item in right_list:
        num_occurs[item] += 1

    ans = 0
    for item in left_list:
        ans += item * num_occurs[item]

    return ans

def solve(lines: Lines) -> int:
    """Solve the problem."""
    left_list, right_list = parse_lists(lines)

    ans = 0
    for item1, item2 in zip(sorted(left_list), sorted(right_list)):
        ans += abs(item1 - item2)
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
    assert result == 2769675
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
