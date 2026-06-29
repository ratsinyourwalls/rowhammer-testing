import math


class GrapheneProtector:
    def __init__(self, controller):
        self.controller = controller

        # After how many accesses should we refresh?
        self.treshold = controller.get_treshold() / 2
        # On refresh triggeered, distance of neighbours to refresh
        self.ref_dist = 1

        # table_size > (refreshcycle / treshold) - 1
        # size of the misra table for each bank
        # Formula given by the paper
        self.table_size = (
            math.ceil(controller.refreshcycle / (controller.get_treshold()/2)) + 10
        )

        banks = controller.get_banks()
        self.misra = []
        for _ in range(banks):
            self.misra.append(MisraGries(self.table_size))

    # Write event
    def notify_read(self, bank, row):
        self.misra[bank].add(row)
        t = self.misra[bank].get(row)

        # We refresh if the count is a multiple of treshold
        if t > 0 and (t % self.treshold == 0):
            print(f"GRAPHENE: Triggered refresh from {bank}:{row}, t={t}")

            # Refresh rows at increasing distance
            for d in range(self.ref_dist):
                self.controller.safety_refresh(bank, row + (d + 1))
                self.controller.safety_refresh(bank, row - (d + 1))

    # Refresh event
    def notify_refresh(self, bank):
        # Just reset the misra count of the bank with a blank one
        self.misra[bank] = MisraGries(self.table_size)


# Implements the Misra Gries algorithm from the paper
class MisraGries:
    def __init__(self, size):
        # Maximum number of keys in the table
        self.size = size

        # The table is a dict of keys and their approximate count
        self.table = {}

        # The spillover is a count of all the elements that don't go
        # in the table, because the keys are missing.
        self.spillover = 0

    # Encountered element "key", add it to the frequency table
    def add(self, key):
        # If already present in the table, just add one to the freq
        if key in self.table:
            self.table[key] += 1
        # If the table isn't full, add it to the table
        elif len(self.table) < self.size:
            self.table[key] = self.spillover + 1
        # Not found and no space
        else:
            # If we find an element whith count = spillover we replace it,
            # otherwise increase spillover
            found = False
            for k, c in self.table.items():
                if c == self.spillover:
                    # Found the element to replace
                    self.table.pop(k)
                    self.table[key] = self.spillover + 1
                    found = True
                    break
            if not found:
                self.spillover += 1

    # Get an approximate count
    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return 0
