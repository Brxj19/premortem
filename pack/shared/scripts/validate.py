#!/usr/bin/env python3
"""Validate a failure-tree.json file."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Validate failure-tree.json")
    parser.add_argument("tree", help="Path to failure-tree.json")
    parser.add_argument("--candidates", help="Path to candidates.json")
    parser.add_argument("--rescore", action="store_true", help="Recompute scores")
    parser.add_argument("--strict", action="store_true", help="Fail on unreviewed findings")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()
    print("validate.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
