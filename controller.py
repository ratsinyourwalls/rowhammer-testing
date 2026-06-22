from memory import Memory
from gui import MemoryGUI as gui

# We are simulating a model where only reads happen, no writes. Every bit is zero.
# When a bit flips it becomes 1


class MemoryController:
    # The MemoryController will refresh every refreshcycle writes or skips.
    def __init__(self, banks, banksize, refreshcycle):
        self.memory = Memory(banks, banksize, refreshcycle * 0.15)
        self.refreshcycle = refreshcycle
        self.readcounts = [0] * banks
        self.protector = None
        self.gui = None

        # useful for statistics
        self.stat_reads = [0] * banks
        self.stat_safety_refresh = [0] * banks
        self.stat_refresh = [0] * banks
        # self.stat_flips = [0] * banks

    def register_protector(self, protector):
        self.protector = protector

    def register_gui(self, gui):
        self.gui = gui
        self.memory.register_gui(gui)

    def read(self, bank, row):
        self.stat_reads[bank] += 1

        # refresh every tot reads on a bank
        self.readcounts[bank] += 1
        if self.protector:
            self.protector.notify_read(bank, row)

        self.memory.read(bank, row)
        if self.readcounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    def safety_refresh(self, bank, row):
        self.stat_safety_refresh[bank] += 1
        self.memory.read(bank, row)
        self.gui.notify_refresh(bank, row)

    # As the MemoryController has no conception of time, we will need to call
    # skip to simulate cycles where it doesn't write
    def skip(self, bank):
        self.readcounts[bank] += 1

        if self.readcounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    def refresh(self, bank):
        self.stat_refresh[bank] += 1
        if self.protector:
            self.protector.notify_refresh(bank)

        self.readcounts[bank] = 0
        self.memory.refresh(bank)

    def refresh_all(self):
        for bank in range(self.get_banks()):
            self.refresh(bank)

    def get_banks(self):
        return self.memory.get_banks()

    def get_banksize(self):
        return self.memory.get_banksize()

    def get_stat_reads(self, bank):
        return self.stat_reads[bank]

    def get_stat_refresh(self, bank):
        return self.stat_refresh[bank]

    def get_stat_safety_refresh(self, bank):
        return self.stat_safety_refresh[bank]

    def get_stat_flips(self, bank):
        return self.memory.get_stat_flips(bank)

    def reset_stats(self):
        banks = self.get_banks()
        self.stat_reads = [0] * banks
        self.stat_safety_refresh = [0] * banks
        self.stat_refresh = [0] * banks
        self.memory.reset_stat_flips()
    
