import math


class Protector:
    def __init__(self, controller):
        self.controller = controller
        self.treshold = 50
        # table_size > (refreshcycle / treshold) - 1
        self.table_size = math.ceil(controller.refreshcycle / self.treshold) + 1
        self.ref_dist = 1

        banks = controller.get_banks()
        self.misra = []
        for _ in range(banks):
            self.misra.append(MisraGries(self.table_size))

    # Write event
    def notify_read(self, bank, row):
        self.misra[bank].add(row)
        if self.check_treshold(self.misra[bank].get(row)):
            print(f"GRAPHENE: Triggered refresh from {bank}:{row}")
            for d in range(self.ref_dist):
                self.controller.refresh_row(bank, row + (d + 1))
                self.controller.refresh_row(bank, row - (d + 1))

    # Refresh event
    def notify_refresh(self, bank):
        self.misra[bank] = MisraGries(self.table_size)

    def check_treshold(self, t):
        i = 1
        while t > self.treshold * i:
            i += 1
        if t == self.treshold * i:
            return True
        else:
            return False


class MisraGries:
    def __init__(self, size):
        self.size = size
        self.table = {}
        self.spillover = 0

    def add(self, key):
        if key in self.table:
            self.table[key] += 1
        elif len(self.table) < self.size:
            self.table[key] = self.spillover + 1
        else:
            found = False
            for k, c in self.table.items():
                if c == self.spillover:
                    self.table.pop(k)
                    self.table[key] = self.spillover + 1
                    found = True
                    break
            if not found:
                self.spillover += 1

    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return 0

    def remove(self, key):
        if key in self.table:
            self.table.pop(key)
