#!/usr/bin/env python3
"""Detect entities, call sites and failure modes in a codebase."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Detect entities and failure modes")
    parser.add_argument("root", help="Root directory to scan")
    parser.add_argument("--scope", nargs="*", help="Limit scan to these paths")
    parser.add_argument("--entry", nargs="*", help="Limit to entry points")
    parser.add_argument("--lang", default="python,typescript", help="Languages to scan")
    parser.add_argument("--exclude", nargs="*", help="Glob patterns to exclude")
    parser.add_argument("--resilience", help="Path to resilience.json")
    parser.add_argument("--out", default="premortem-out", help="Output directory")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()
    print("detect.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
