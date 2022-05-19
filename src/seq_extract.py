import argparse
import sys
import random


def uniform_extraction(parent_sequence, min_length, max_length):
    min_length = 0 if min_length is None else min_length
    max_length = len(parent_sequence) if max_length is None else max_length
    seq_length = random.randint(min_length, max_length)
    index = random.randint(0, len(parent_sequence) - seq_length)
    return parent_sequence[index: index + seq_length]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("parent_sequence", type=str)
    parser.add_argument("--min-length", type=int)
    parser.add_argument("--max-length", type=int)
    args = parser.parse_args(sys.argv[1:])

    seq = uniform_extraction(args.parent_sequence, args.min_length, args.max_length)

    print(seq)


if __name__ == "__main__":
    main()
