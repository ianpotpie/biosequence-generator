import random
import argparse
import sys

DNA_SYMBOLS = ["A", "C", "G", "T"]
RNA_SYMBOLS = ["A", "C", "G", "T", "U"]
PROTEIN_SYMBOLS = ["A", "G", "I", "L", "P", "V", "F", "W", "Y", "D",
                   "E", "R", "H", "K", "S", "T", "C", "M", "N", "Q"]


def extract_sequence(parent_sequence, prior, error_rate, insertion_rate, deletion_rate, symbols):
    insertion_open, insertion_extend = insertion_rate
    deletion_open, deletion_extend = deletion_rate
    state = random.choices(["M", "I", "D"], prior, k=1)[0]

    extracted_sequence = ""
    for symbol in parent_sequence:
        if state == "M":
            if random.random() <= error_rate:
                extracted_sequence += random.choices(symbols, [s != symbol for s in symbols])[0]
            else:
                extracted_sequence += symbol
            state = random.choices(["M", "I", "D"], [1 - (insertion_open + deletion_open),
                                                     insertion_open, deletion_open])[0]

        elif state == "I":
            extracted_sequence += random.choice(symbols)
            while random.random() <= insertion_extend:
                extracted_sequence += random.choice(symbols)
            state = "M"

        else:  # state == "D"
            if random.random() > insertion_extend:
                state = "M"

    return extracted_sequence


def main():
    parser = argparse.ArgumentParser(prog="Sequence Extractor",
                                     description="Uses a hidden-markov-like model in order to generate a new sequence "
                                                 "from a parent state. The model has 3 states. The deletion state "
                                                 "iterates over the parent sequence without producing symbols. The"
                                                 "insertion state produces symbols without iterating over the parent "
                                                 "sequence. Finally, the match/mismatch state produces symbols as it "
                                                 "iterates over the parent sequence with some probability of error.")
    parser.add_argument("parent_sequence",
                        help="The parent/source sequence from which our extracted sequence will be taken")
    parser.add_argument("--prior", "-p", type=float, nargs=3, default=[1.0, 0.0, 0.0],
                        help="The probability of beginning in each state (match/insert/insert respectively).")
    parser.add_argument("--matrix", "-m", type=str,
                        help="This substitution matrix file encodes the probability of reading each symbol given the "
                             "\"true\" symbol.")
    parser.add_argument("--error-rate", "-e", type=float, default=0.1,
                        help="If a substitution matrix is not provided, then we uniformly choose between non-matching"
                             "symbols with the provided probability.")
    parser.add_argument("--insertion-rate", "-i", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the insertion state and the probability of remaining"
                             "in the insertion state once there (the probability of extending the insertion)")
    parser.add_argument("--deletion-rate", "-d", type=float, nargs=2, default=[0.0, 0.0],
                        help="The probability of transitioning to the deletion state and the probability of remaining"
                             "in the deletion state once there (the probability of extending the deletion)")
    parser.add_argument("--type", "-t", type=str, choices=["DNA", "RNA", "PROTEIN"], default="PROTEIN",
                        help="Defines which biosequence symbols to use in the sequencing.")
    args = parser.parse_args(sys.argv[1:])

    if args.type == "DNA":
        symbols = DNA_SYMBOLS
    elif args.type == "RNA":
        symbols = RNA_SYMBOLS
    else:  # args.type == PROTEIN
        symbols = PROTEIN_SYMBOLS

    new_sequence = extract_sequence(args.parent_sequence, args.prior, args.error_rate,
                                    args.insertion_rate, args.deletion_rate, symbols)
    print(new_sequence)


if __name__ == "__main__":
    main()
