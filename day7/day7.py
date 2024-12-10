#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 7
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
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        """,
        3749
    ),
]

SAMPLE_CASES2 = [
    (
        """
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        """,
        11387
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
def parse_equations(lines):
    new_lines = []
    for line in lines:
        LHS = int(line.split(':')[0])
        RHS = [int(param) for param in line.split(':')[1].strip().split()]
        new_lines.append((LHS, RHS))
    return new_lines

def equation_possible(LHS, RHS, acc):
    if not RHS:
        if acc == LHS:
            return True
    else:
        curr_param = RHS[0]
        rest_RHS   = RHS[1:]
        add_possible  = equation_possible(LHS, rest_RHS, acc + curr_param) 
        mult_possible = equation_possible(LHS, rest_RHS, acc * curr_param) 
        return add_possible or mult_possible
    return False

def equation_possible_with_concat(LHS, RHS, acc):
    if not RHS:
        if acc == LHS:
            return True
    else:
        curr_param = RHS[0]
        rest_RHS   = RHS[1:]
        add_possible    = equation_possible_with_concat(LHS, rest_RHS, acc + curr_param) 
        mult_possible   = equation_possible_with_concat(LHS, rest_RHS, acc * curr_param) 
        concat_possible = equation_possible_with_concat(LHS, rest_RHS, int(f"{acc}{curr_param}"))
        return add_possible or mult_possible or concat_possible
    return False

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    lines = parse_equations(lines)
    ans = 0
    for LHS, RHS in lines:
        if equation_possible_with_concat(LHS, RHS, 0):
            ans += LHS
    return ans


def solve(lines: Lines) -> int:
    """Solve the problem."""
    lines = parse_equations(lines)
    ans = 0
    for LHS, RHS in lines:
        if equation_possible(LHS, RHS, 0):
            ans += LHS
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
    assert result == 42283209483350
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
