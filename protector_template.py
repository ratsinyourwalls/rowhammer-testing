# Protector framework
# TODO implement protector strategies
class Protector:
    def __init__(self, controller):
        self.controller = controller

    # Write event
    def notify_read(self, bank, row):
        pass

    # Refresh event
    def notify_refresh(self, bank):
        pass
