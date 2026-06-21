import random


class ParaProtector:
    def __init__(self, controller):
        self.controller = controller
        # Random chance of refreshing neighbours on read
        self.ref_p = 0.01
        # Distance of neighbours to refresh
        self.ref_dist = 1

    # Write event
    def notify_read(self, bank, row):
        if random.random() < self.ref_p:
            print("PARA: Random refresh")
            # Refresh all neighbours at the right distances..
            for d in range(self.ref_dist):
                self.controller.safety_refresh(bank, row + (d + 1))
                self.controller.safety_refresh(bank, row - (d + 1))

    # Refresh event
    def notify_refresh(self, bank):
        # dont care
        pass
