from memory import Memory


class MemoryController:
    # The MemoryController will refresh every refreshcycle writes or skips.
    def __init__(self, banks, banksize, refreshcycle):
        self.memory = Memory(banks, banksize)
        self.refreshcycle = refreshcycle
        self.writecounts = [0] * banks
        self.protector = None

    def register_protector(self, protector):
        self.protector = protector

    def write(self, bank, row):
        # TODO is keeping count realistic? Are we sure we want to separate the protector
        # and controller logic?
        self.writecounts[bank] += 1
        # TODO implement write blocking with a queue? or just a refresh ig
        if self.protector:
            self.protector.notifywrite(bank, row)

        self.memory.write(bank, row)
        if self.writecounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    # As the MemoryController has no conception of time, we will need to call
    # skip to simulate cycles where it doesn't write
    def skip(self, bank):
        self.writecounts[bank] += 1

        if self.writecounts[bank] >= self.refreshcycle:
            self.refresh(bank)

    def refresh(self, bank):
        if self.writecounts[bank] >= self.refreshcycle:
            self.update_stats()
            if self.protector:
                self.protector.notifyrefresh()

            self.writecounts[bank] = 0
            self.memory.refresh(bank)

    def get_banks(self):
        return self.memory.get_banks()

    def get_banksize(self):
        return self.memory.get_banksize()

    # I don't understand how flip works and I don't understand
    # why we're summing TODO ask sofia
    def get_flip_number(self, bank):
        flip = 0
        for row in range(self.get_banksize()):
            s = self.memory.flip_probability(bank, row)
            if s > 0.5:
                flip += 1
        return flip

    # Will be called once each refresh.
    def update_stats(self):
        # TODO generate a report somehow
        pass
