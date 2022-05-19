import random
import argparse
import sys

DNA_SYMBOLS = ["A", "C", "G", "T"]
RNA_SYMBOLS = ["A", "C", "G", "T", "U"]
PROTEIN_SYMBOLS = ["A", "G", "I", "L", "P", "V", "F", "W", "Y", "D",
                   "E", "R", "H", "K", "S", "T", "C", "M", "N", "Q"]
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


def mutate_sequence(sequence, symbols, error_rate, prior=None, insertion_rates=None, deletion_rates=None):
    """
    Mutate a sequence with mismatches, insertions, and deletions based on the mechanisms of an HMM.

    :param sequence: the sequence to mutate
    :param symbols: the symbols available for insertion (the alphabet of the sequence)
    :param error_rate: the rate that mismatching occurs
    :param prior: the prior distribution over mismatch, insertion, and deletion states
    :param insertion_rates: the opening and extension probabilities of an insertion
    :param deletion_rates: the opening and extension probabilities of a deletion
    :return: the new mutated sequence
    """
    insertion_open, insertion_extend = (0.0, 0.0) if insertion_rates is None else insertion_rates
    deletion_open, deletion_extend = (0.0, 0.0) if deletion_rates is None else deletion_rates
    state = "M" if prior is None else random.choices(["M", "I", "D"], prior, k=1)[0]

    mutated_sequence = ""
    for symbol in sequence:
        if state == "M":
            if random.random() <= error_rate:
                mutated_sequence += random.choices(symbols, [s != symbol for s in symbols])[0]
            else:
                mutated_sequence += symbol
            state = random.choices(["M", "I", "D"], [1 - (insertion_open + deletion_open),
                                                     insertion_open, deletion_open])[0]

        elif state == "I":
            mutated_sequence += random.choice(symbols)
            while random.random() <= insertion_extend:
                mutated_sequence += random.choice(symbols)
            state = "M"

        else:  # state == "D"
            if random.random() > insertion_extend:
                state = "M"

    return mutated_sequence


def main():
    description = "Uses a hidden-markov-like model in order to generate a new sequence from a parent state. The " \
                  "model has 3 states. The deletion state iterates over the parent sequence without producing " \
                  "symbols. The insertion state produces symbols without iterating over the parent sequence. " \
                  "Finally, the match/mismatch state produces symbols as it iterates over the parent sequence with " \
                  "some probability of error."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("sequence",
                        help="The sequence to be mutated")
    parser.add_argument("--prior", "-p", type=float, nargs=3,
                        help="The probability of beginning in each state (match/insert/insert respectively).")
    parser.add_argument("--matrix", "-m", type=str,
                        help="This substitution matrix file encodes the probability of reading each symbol when an "
                             "error occurs given the original symbol")
    parser.add_argument("--error-rate", "-e", type=float, default=0.1,
                        help="If a substitution matrix is not provided, then we uniformly choose between non-matching"
                             "symbols with the provided probability.")
    parser.add_argument("--insertion-rate", "-i", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the insertion state and the probability of remaining"
                             "in the insertion state once there (the probability of extending the insertion)")
    parser.add_argument("--deletion-rate", "-d", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the deletion state and the probability of remaining"
                             "in the deletion state once there (the probability of extending the deletion)")
    parser.add_argument("--type", "-t", type=str, choices=["DNA", "RNA", "PROTEIN", "ALPHABET"], default="PROTEIN",
                        help="Defines which biosequence symbols to use in the sequencing.")
    args = parser.parse_args(sys.argv[1:])

    if args.type == "DNA":
        symbols = DNA_SYMBOLS
    elif args.type == "RNA":
        symbols = RNA_SYMBOLS
    elif args.type == "PROTEIN":
        symbols = PROTEIN_SYMBOLS
    else:
        symbols = ALPHABET

    new_sequence = mutate_sequence(args.sequence, symbols, args.error_rate, args.prior,
                                   args.insertion_rate, args.deletion_rate)

    print(new_sequence)


if __name__ == "__main__":
    main()
