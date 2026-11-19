#!/usr/bin/env python3
"""Query a failure tree for what-if, blast radius and other questions."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Query the failure tree")
    parser.add_argument("command", help="Query command",
                        choices=["blast-radius", "what-if", "silent", "critical",
                                 "spof", "path", "finding", "entities", "workflows"])
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--tree", default="premortem-out/failure-tree.json", help="Path to failure-tree.json")
    parser.add_argument("--band", default="critical", help="Band filter for critical command")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()
    print("query.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
