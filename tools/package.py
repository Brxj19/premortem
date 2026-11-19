#!/usr/bin/env python3
"""Build dist/premortem-lite.zip and dist/premortem-pro.zip from pack/."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Package Premortem for Agensi")
    parser.add_argument("--variant", required=True, choices=["lite", "pro"])
    parser.add_argument("--layout", default="pack", choices=["pack", "flat"])
    args = parser.parse_args()
    print("package.py: not yet implemented", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
