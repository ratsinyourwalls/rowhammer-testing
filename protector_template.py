# Protector framework
# TODO implement protector strategies
class Protector:
    def __init__(self, controller):
        self.controller = controller

    # Write event
    def notifyread(self, bank, row):
        pass

    # Refresh event
    def notify_refresh(self, bank):
        pass
