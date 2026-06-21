import random


class Protector:
    def __init__(self, controller):
        self.controller = controller
        self.ref_p = 0.001
        self.ref_dist = 1

    # Write event
    def notify_read(self, bank, row):
        if random.random() < self.ref_p:
            print("PARA: Random refresh")
            for d in range(self.ref_dist):
                self.controller.refresh_row(bank, row + (d + 1))
                self.controller.refresh_row(bank, row - (d + 1))

    # Refresh event
    def notify_refresh(self, bank):
        pass
