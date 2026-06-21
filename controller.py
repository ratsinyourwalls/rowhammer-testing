import random
from memory import Memory
from gui import MemoryGUI as gui

# We are simulating a model where only reads happen, no writes. Every bit is zero.
# When a bit flips it becomes 1


class MemoryController:
    # The MemoryController will refresh every refreshcycle writes or skips.
    def __init__(self, banks, banksize, refreshcycle):
        self.memory = Memory(banks, banksize)
        self.refreshcycle = refreshcycle
        self.readcounts = [0] * banks
        self.protector = None
        self.gui = None

    def register_protector(self, protector):
        self.protector = protector

    def register_gui(self, gui):
        self.gui = gui
        self.memory.register_gui(gui)

    def read(self, bank, row):
        # refresh every tot reads on a bank
        self.readcounts[bank] += 1
        if self.protector:
            self.protector.notify_read(bank, row)

        self.memory.read(bank, row)
        if self.readcounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    def refresh_row(self, bank, row):
        self.memory.read(bank, row)
        gui.notify_refresh(bank, row)

    # As the MemoryController has no conception of time, we will need to call
    # skip to simulate cycles where it doesn't write
    def skip(self, bank):
        self.readcounts[bank] += 1

        if self.readcounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    def refresh(self, bank):
        self.update_stats()
        if self.protector:
            self.protector.notify_refresh(bank)
        if self.gui:
            self.gui.notify_refresh(bank)

        self.readcounts[bank] = 0
        self.memory.refresh(bank)

    def refresh_all(self):
        for bank in range(self.get_banks()):
            self.refresh(bank)

    def get_banks(self):
        return self.memory.get_banks()

    def get_banksize(self):
        return self.memory.get_banksize()

    # TODO consider getting rid of this
    # TODO consider changing it for something else
    def get_flip_number(self, bank):
        flips = 0
        for row in range(self.get_banksize()):
            p = self.memory.flip_probability(bank, row)
            if p > random.random():
                print("FLIP at", bank, row)
                print("Probability", p, "near accesses:", self.memory.get_ac(bank, row))
                self.gui.notify_flip(bank, row)
                flips += 1
        return flips

    # Will be called once each refresh.
    def update_stats(self):
        # TODO generate a report somehow
        pass
