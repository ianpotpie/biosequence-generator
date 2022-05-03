import numpy as np


class SubstitutionMatrix:
    def __init__(self, matrix_file, scale):
        # TODO: we can find these values using:
        # sum[i,j]( p_i p_j exp(lambda * s[i,j]) )= 1
        self.scale = scale
        self.symbol_to_prior = None
        self.symbol_to_index = None
        self.scoring_matrix = None

        with open(matrix_file, mode='r') as f:
            headline = f.readline()
            while headline[0] == "#":  # iterates past all lines with comments
                headline = f.readline()
            self.symbol_to_index = {symbol.strip(): i for i, symbol in enumerate(headline.split())}

            # fill the scoring matrix
            n_symbols = len(self.symbol_to_index)
            self.scoring_matrix = np.zeros((n_symbols, n_symbols))
            for line in f:
                row = line.split()
                symbol = row.pop(0)
                i = self.symbol_to_index[symbol]
                for j, score in enumerate(row):
                    self.scoring_matrix[i, j] = float(score)

    def get_symbols(self):
        """
        Creates a list of all symbols in the scoring matrix in the order in which they appear.
        Returns none if no scoring matrix has been loaded.

        :return: a list of symbols
        """
        if self.scoring_matrix is None:
            return None
        else:
            symbols = np.empty(len(self.symbol_to_index), dtype=str)
            for symbol, index in self.symbol_to_index.items():
                symbols[index] = symbol
            return list(symbols)

    def __str__(self):
        """
        Creates a string representation of the scoring scheme.
        If a scoring matrix is loaded, then it uses a standard PAM or BLOSUM style matrix.

        :return: a string of the scoring scheme
        """
        s = ""
        symbols = self.get_symbols()
        s += "   " + "  ".join(symbols)
        for i in range(self.scoring_matrix.shape[0]):
            s += "\n" + symbols[i]
            for j in range(self.scoring_matrix.shape[1]):
                score = self.scoring_matrix[i, j]
                score = int(score) if score.is_integer() else score
                s += f" {score}" if score < 0.0 else f"  {score}"

        return s
