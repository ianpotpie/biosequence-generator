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
    ins_open, ins_extend = (0.0, 0.0) if insertion_rates is None else insertion_rates
    del_open, del_extend = (0.0, 0.0) if deletion_rates is None else deletion_rates
    state = "M" if prior is None else random.choices(["M", "I", "D"], prior, k=1)[0]
    substitution = 1 - (ins_open + del_open)

    ins_to_sub = (1 - ins_extend) * substitution / (substitution + del_open)
    ins_to_del = (1 - ins_extend) * del_open / (substitution + del_open)
    del_to_sub = (1 - ins_extend) * substitution / (substitution + ins_open)
    del_to_ins = (1 - ins_extend) * ins_open / (substitution + ins_open)

    mutated_sequence = ""
    index = 0
    while index < len(sequence) or state == "I":
        if state == "M":
            symbol = sequence[index]
            error = random.choices(symbols, [s != symbol for s in symbols])[0]
            mutated_sequence += symbol if random.random() > error_rate else error
            state = random.choices(["M", "I", "D"], [substitution, ins_open, del_open])[0]
            index += 1

        elif state == "I":
            mutated_sequence += random.choice(symbols)
            state = random.choices(["M", "I", "D"], [ins_to_sub, ins_extend, ins_to_del])[0]

        else:  # state == "D"
            state = random.choices(["M", "I", "D"], [del_to_sub, del_to_ins, del_extend])[0]
            index += 1

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
    parser.add_argument("--insertion-rates", "-i", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the insertion state and the probability of remaining"
                             "in the insertion state once there (the probability of extending the insertion)")
    parser.add_argument("--deletion-rates", "-d", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the deletion state and the probability of remaining"
                             "in the deletion state once there (the probability of extending the deletion)")
    parser.add_argument("--alphabet", "-a", type=str, choices=["DNA", "RNA", "PROTEIN", "ALPHABET"], default="PROTEIN",
                        help="Defines which biosequence symbols to use in the sequencing.")
    args = parser.parse_args(sys.argv[1:])

    if args.alphabet == "DNA":
        symbols = DNA_SYMBOLS
    elif args.alphabet == "RNA":
        symbols = RNA_SYMBOLS
    elif args.alphabet == "PROTEIN":
        symbols = PROTEIN_SYMBOLS
    else:
        symbols = ALPHABET

    new_sequence = mutate_sequence(args.sequence, symbols, args.error_rate, args.prior,
                                   args.insertion_rates, args.deletion_rates)

    print(new_sequence)


if __name__ == "__main__":
    main()
