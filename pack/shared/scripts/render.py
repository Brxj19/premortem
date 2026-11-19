#!/usr/bin/env python3
"""Render failure-tree.json to FAILURES.md and Mermaid diagrams."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Render failure tree to Markdown and Mermaid")
    parser.add_argument("tree", help="Path to failure-tree.json")
    parser.add_argument("--out", default="premortem-out", help="Output directory")
    parser.add_argument("--top", type=int, default=20, help="Max top risks to show")
    parser.add_argument("--format", default="md,mmd", help="Output formats")
    args = parser.parse_args()
    print("render.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
