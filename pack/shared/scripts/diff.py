#!/usr/bin/env python3
"""Diff two versions of a codebase for new or changed failure modes."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Diff failure modes between git refs")
    parser.add_argument("--base", required=True, help="Base git ref")
    parser.add_argument("--head", default="HEAD", help="Head git ref (default: HEAD)")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--out", default="premortem-out", help="Output directory")
    parser.add_argument("--fail-on", choices=["critical", "high"], help="Exit 1 if findings at this band or above")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()
    print("diff.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
