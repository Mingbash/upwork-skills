#!/usr/bin/env python3
"""Count Unicode code points; optionally enforce a caller-supplied inclusive cap."""
import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-chars', type=int, default=None)
    parser.add_argument('descriptions', nargs='+')
    args = parser.parse_args()
    if args.max_chars is not None and args.max_chars < 1:
        parser.error('--max-chars must be a positive integer')
    valid = True
    for index, text in enumerate(args.descriptions, 1):
        count = len(text)
        good = bool(text.strip()) and (args.max_chars is None or count <= args.max_chars)
        status = 'FAIL' if not good else 'NOT_ENFORCED' if args.max_chars is None else 'PASS'
        print(f'{index}: {status} ({count} code points)')
        valid = valid and good
    return 0 if valid else 1

if __name__ == '__main__':
    raise SystemExit(main())
