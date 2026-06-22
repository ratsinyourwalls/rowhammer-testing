import random

"""
This doesn't store the values, it only keeps track of certain events
The events are access, probability of flip, and whether a row has had a flip.
"""


class Memory:
    # A memory has banks, independent banks, and banksize rows whithin each one
    def __init__(self, nbanks, banksize, treshold):
        # blank memory
        # number of banks and size
        self.banks = nbanks
        self.banksize = banksize
        # number of accesses to a certain cell
        self.accesses = [[0] * banksize for _ in range(nbanks)]
        # probability of flip
        self.probs = [[0] * banksize for _ in range(nbanks)]
        # whether a row has had a flip.
        self.flipped = [[False] * banksize for _ in range(nbanks)]
        self.gui = None

        self.stat_flips = [0] * nbanks
        self.treshold = treshold

    # return number of banks
    def get_banks(self):
        return self.banks

    # number of rows in a bank
    def get_banksize(self):
        return self.banksize

    # return access counter
    def get_ac(self, bank, row):
        # excluding out of bounds
        if (
            bank < 0
            or bank >= self.get_banks()
            or row < 0
            or row >= self.get_banksize()
        ):
            return 0
        return self.accesses[bank][row]

    def register_gui(self, gui):
        self.gui = gui

    # just puts all bits back to 0
    # this represents resetting the activation counter
    def refresh(self, bank):
        # print("MEMORY REFRESH")
        self.accesses[bank] = [0] * self.get_banksize()
        self.probs[bank] = [0] * self.get_banksize()
        # flips shouldn't get erased on refresh
        # self.flipped[bank] =[False] * self.get_banksize()

    def reset(self):
        print("FLIP RESET")
        for bank in range(self.get_banks()):
            self.flipped[bank] = [False] * self.get_banksize()
            # self.stat_flips[bank] = 0
            self.refresh(bank)

    # read doesn't actually read the value, it counts one access to the row
    def read(self, bank, row):
        if bank < 0 or bank >= self.banks or row < 0 or row >= self.banksize:
            # print("Out of bounds:", bank, row)
            return
        self.accesses[bank][row] += 1
        self.probs[bank][row] = 0
        self.update_neighbours(bank, row)

    def update_neighbours(self, bank, row):
        if not self.gui.is_multi_row():
            weights = [1]
        else:
            weights = [1, 0.5, 0.2]
        for dist, w in enumerate(weights):
            self.update_probability(bank, row + (dist + 1), w)
            self.update_probability(bank, row - (dist + 1), w)

    def update_probability(self, bank, row, weight):
        if (
            bank < 0
            or bank >= self.get_banks()
            or row < 0
            or row >= self.get_banksize()
        ):
            return
        if self.flipped[bank][row]:
            return
        self.probs[bank][row] += weight
        p = self.flip_probability(bank, row)
        if p > random.random():
            print("FLIP at", bank, row)
            print("Probability:", p, "row accesses:", self.accesses[bank][row])

            self.stat_flips[bank] += 1
            self.gui.notify_flip(bank, row)
            self.flipped[bank][row] = True

    def flip_probability(self, bank, row):
        if (row + bank * 7) % 3 != 1 and (row + bank * 20) % 5 != 2:
            return 0

        MAXW = self.treshold / 2

        w = self.probs[bank][row]
        if w < self.treshold:
            return 0
        else:
            return min((w - self.treshold) / MAXW, 1.0)

    def get_stat_flips(self, bank):
        return self.stat_flips[bank]

    def reset_stat_flips(self):
        self.stat_flips = [0] * self.banks
