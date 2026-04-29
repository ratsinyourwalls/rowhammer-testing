class Memory:
    # A memory has banks independent banks, and banksize rows whithin each one
    def __init__(self, banks, banksize):
        self.banks = [] * banks
        for i in range(banks):
            self.banks[i] = [0] * banksize

    def get_banks(self):
        return len(self.banks)

    def get_banksize(self):
        return len(self.banks[0])

    def read(self, bank, row):
        if bank < 0 or bank > self.get_banks() or row < 0 or row > self.get_banksize():
            return 0
        return self.banks[bank][row]

    def refresh(self):
        for i in range(self.get_banks()):
            self.banks[i] = [0] * self.get_banksize()

    def write(self, bank, row):
        self.banks[bank][row] += 1

    def flip_probability(self, bank, row):
        # TODO change the probabilities to something reasonable (and not
        # hardcoded)
        probabilities = [0.1, 0.01, 0.001]

        s = 0
        for i, p in enumerate(probabilities):
            s += p * self.read(bank, row + (i + 1))
            s += p * self.read(bank, row - (i + 1))

        return s
