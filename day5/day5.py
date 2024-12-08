#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 5
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
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
        """,
        143
    ),
]

SAMPLE_CASES2 = [
    (
        """
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
        """,
        123
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

def parse_input(lines):
    rule_entries, update_entries = parse_sections(lines)
    rules = {}
    for rule_entry in rule_entries:
        entry, update_before = rule_entry.split('|')
        entry = int(entry)
        update_before = int(update_before)
        if rules.get(entry):
            rules[entry].add(update_before)
        else:
            rules[entry] = {update_before}
    updates = []
    for update_entry in update_entries:
        updates.append([int(entry) for entry in update_entry.split(',')])
    return rules, updates

# Solution
def is_update_valid(rules, update):
    seen_objs = []
    for item in update:
        for seen_obj in seen_objs:
            if rules.get(item) and seen_obj in rules.get(item):
                return False
        seen_objs.append(item)
    return True

def sort_update(rules, update):
    while not is_update_valid(rules, update):
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                # swap if they are out of order
                if rules.get(update[j]) and update[i] in rules.get(update[j]):
                    update[i], update[j] = update[j], update[i]
    return update

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    rules, updates = parse_input(lines)
    ans = 0
    for update in updates:
        if not is_update_valid(rules, update):
            sorted_update = sort_update(rules, update)
            ans += sorted_update[len(update) // 2]
    return ans

def solve(lines: Lines) -> int:
    """Solve the problem."""
    rules, updates = parse_input(lines)
    ans = 0
    for update in updates:
        if is_update_valid(rules, update):
            ans += update[len(update) // 2]
    return ans


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text, blank_lines=True)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 5651
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text, blank_lines=True)
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
    input_lines = load_input(INPUTFILE, blank_lines=True)
    part1(input_lines)
    example2()
    part2(input_lines)
