from memory import Memory


class MemoryController:
    # The MemoryController will refresh every refreshcycle writes or skips.
    def __init__(self, banks, banksize, refreshcycle):
        self.memory = Memory(banks, banksize)
        self.refreshcycle = refreshcycle
        self.writecount = 0

    def write(self, bank, row):
        self.writecount += 1
        if self.writecount >= self.refreshcycle:
            self.refresh()
        self.memory.write(bank, row)

    # As the MemoryController has no conception of time, we will need to call
    # skip to simulate cycles where it doesn't write
    def skip(self):
        self.writecount += 1
        if self.writecount >= self.refreshcycle:
            self.refresh()

    def refresh(self):
        self.update_stats()
        if self.writecount >= self.refreshcycle:
            self.writecount = 0
            self.memory.refresh()

    def get_banks(self):
        return self.memory.get_banks()

    def get_banksize(self):
        return self.memory.get_banksize()

    def get_flip_number(self):
        flip = 0
        for bank in range(self.get_banks()):
            for row in range(self.get_banksize()):
                s = self.memory.flip_probability(bank, row)
                if s > 0.5:
                    flip += 1
        return flip

    # Will be called once each refresh.
    def update_stats(self):
        # TODO generate a report somehow
        pass
