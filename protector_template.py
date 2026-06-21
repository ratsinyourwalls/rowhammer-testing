# Protector framework
"""
Does nothing
"""
class DefaultProtector:
    def __init__(self, controller):
        self.controller = controller

    # Write event
    def notify_read(self, bank, row):
        print("Read notified", bank, row)
        pass

    # Refresh event
    def notify_refresh(self, bank):
        print("Refresh notified", bank)
        pass
