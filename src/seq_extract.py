import argparse
import sys
import random


def uniform_extract(sequence, min_length=None, max_length=None):
    """
    Extract a subsequence of the source sequence with uniformly chosen length and position.

    :param sequence: the source sequence
    :param min_length: the minimum length of the extracted subsequence
    :param max_length: the maximum length of the extracted subsequence
    :return: a subsequence with uniform size and position
    """
    min_length = 0 if min_length is None else min_length
    max_length = len(sequence) if max_length is None else max_length
    seq_length = random.randint(min_length, max_length)
    index = random.randint(min_length, len(sequence) - seq_length)
    subsequence = sequence[index: index + seq_length]
    return subsequence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sequence", type=str)
    parser.add_argument("--min-length", type=int)
    parser.add_argument("--max-length", type=int)
    args = parser.parse_args(sys.argv[1:])

    seq = uniform_extract(args.sequence, args.min_length, args.max_length)

    print(seq)


if __name__ == "__main__":
    main()
