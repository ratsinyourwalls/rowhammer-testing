import random
import time

from controller import MemoryController
from para_protector import Protector
from gui import MemoryGUI

BANKSIZE = 64
controller = MemoryController(banks=4, banksize=BANKSIZE, refreshcycle=1000)
protector = Protector(controller)
controller.register_protector(protector)
gui = MemoryGUI(controller)
controller.register_gui(gui)
# MODES = ["normal", "random", "discover", "attack"]


def normal_access(controller):
    bank = 1

    # stay in the same region
    if random.random() < 0.8:
        row = normal_access.current_row + 1
        if row >= normal_access.region_start + normal_access.region_size:
            row = normal_access.region_start

    elif random.random() < 0.95:
        # print("normal access jump to region start", normal_access.region_start)
        row = normal_access.region_start
    else:
        normal_access.region_size = 30
        max_start = controller.get_banksize() - normal_access.region_size
        normal_access.region_start = random.randint(0, max_start)
        row = normal_access.region_start

    normal_access.current_row = row
    controller.read(bank, row)


# initial region
normal_access.region_start = 0
normal_access.region_size = 100
normal_access.current_row = 0


def random_access(controller):
    bank = 1
    row = random.randint(0, controller.get_banksize() - 1)
    controller.read(bank, row)


def discovery_access(controller):
    bank = 1
    row = discovery_access.current_row
    controller.read(bank, row)

    discovery_access.counter += 1
    if discovery_access.counter >= 300:
        discovery_access.counter = 0
        discovery_access.current_row = (row + 1) % controller.get_banksize()


discovery_access.current_row = 0
discovery_access.counter = 0


def attack_access(controller):
    bank = 1
    row = attack_access.target_row
    if attack_access.hammered_time >= 1000:
        attack_access.target_row = random.randint(0, controller.get_banksize())
        attack_access.hammered_time = 0
        if attack_access.target_row % 2 == 1:
            attack_access.target_row -= 1
    controller.read(bank, row - 1)
    controller.read(bank, row + 1)
    attack_access.hammered_time += 1


attack_access.target_row = 50  # example
attack_access.hammered_time = 0


# TODO generate write sequences and pass them to the controller
# TODO generate some statistics
def main():
    print("Doing casual reads. Maximum expected: 1 flip")
    while gui.running:
        mode = gui.mode
        loopn = 0
        if mode == "normal":
            normal_access(controller)
        elif mode == "random":
            random_access(controller)
        elif mode == "discover":
            discovery_access(controller)
        elif mode == "attack":
            attack_access(controller)
        gui.draw()


if __name__ == "__main__":
    main()
