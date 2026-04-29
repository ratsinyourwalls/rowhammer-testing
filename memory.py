class Memory:
    # A memory has banks, independent banks, and banksize rows whithin each one
    def __init__(self, banks, banksize):
        # blank memory
        self.banks = [[]] * banks
        for i in range(banks):
            self.banks[i] = [0] * banksize

    def get_banks(self):
        return len(self.banks)

    def get_banksize(self):
        return len(self.banks[0])

    def read(self, bank, row):
        # excluding out of bounds
        if bank < 0 or bank > self.get_banks() or row < 0 or row > self.get_banksize():
            return 0
        return self.banks[bank][row]

    # just puts all bits back to 0
    # TODO is this the same thing as memory refresh, for simulation purposes?
    # Let's consider if the refresh does something else then just resetting to previous values
    # or does something eletrical that affects our security measures.
    def refresh(self, bank):
        self.banks[bank] = [0] * self.get_banksize()

    # what does this do?
    def write(self, bank, row):
        self.banks[bank][row] += 1

    def flip_probability(self, bank, row):
        # TODO change the probabilities to something reasonable (and not
        # hardcoded)
        # TODO look up the flip probabilities from the DDR4 studies
        # are those the probabilities for adiacent, distance 2, distance 3?
        probabilities = [0.1, 0.01, 0.001]
        
        # i don't understand this
        s = 0
        for i, p in enumerate(probabilities):
            s += p * self.read(bank, row + (i + 1))
            s += p * self.read(bank, row - (i + 1))

        return s
