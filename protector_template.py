# Protector framework
# TODO implement protector strategies
class Protector:
    def __init__(self, controller):
        self.controller = controller

    # Write event
    def notifywrite(self, bank, row):
        pass

    # Refresh event
    def notifyrefresh(self):
        pass
