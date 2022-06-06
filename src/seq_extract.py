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
    assert 0 <= min_length <= max_length <= len(sequence)

    subseq_length = random.randint(min_length, max_length)
    index = random.randint(min_length, len(sequence) - subseq_length)
    subsequence = sequence[index: index + subseq_length]

    return subsequence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sequence", type=str,
                        help="The sequence from which we are extracting a subsequence")
    parser.add_argument("--min-length", type=int,
                        help="The minimum length of the extracted subsequence")
    parser.add_argument("--max-length", type=int,
                        help="The maximum length of the extracted subsequence")
    args = parser.parse_args(sys.argv[1:])

    subseq = uniform_extract(args.sequence, args.min_length, args.max_length)

    print(subseq)


if __name__ == "__main__":
    main()
