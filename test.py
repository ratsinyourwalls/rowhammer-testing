import random
import time
import sys

from controller import MemoryController
from protector_template import DefaultProtector
from para_protector import ParaProtector
from graphene_protector import GrapheneProtector
from gui import MemoryGUI

BANKSIZE = 64
REFRESHCYCLE = 5000
controller = MemoryController(banks=4, banksize=BANKSIZE, refreshcycle=REFRESHCYCLE)
protector = None
gui = MemoryGUI(controller)
controller.register_gui(gui)


def normal_access(controller, bank):

    # stay in the same region
    if random.random() < 0.8:
        row = normal_access.current_row[bank] + 1
        if row >= normal_access.region_start[bank] + normal_access.region_size[bank]:
            row = normal_access.region_start[bank]

    elif random.random() < 0.95:
        row = normal_access.region_start[bank]
    else:
        normal_access.region_size[bank] = 30
        max_start = controller.get_banksize() - normal_access.region_size[bank]
        normal_access.region_start[bank] = random.randint(0, max_start)
        row = normal_access.region_start[bank]

    normal_access.current_row[bank] = row
    controller.read(bank, row)


# initial region
normal_access.region_start = [0]*4
normal_access.region_size = [100]*4
normal_access.current_row = [0]*4


def random_access(controller, bank):
    row = random.randint(0, controller.get_banksize() - 1)
    controller.read(bank, row)


def discovery_access(controller, bank):
    row = discovery_access.current_row[bank]
    controller.read(bank, row)

    discovery_access.counter[bank] += 1
    if discovery_access.counter[bank] >= 300:
        discovery_access.counter[bank] = 0
        discovery_access.current_row[bank] = (row + 1) % controller.get_banksize()


discovery_access.current_row = [0]*4
discovery_access.counter = [0]*4


def attack_access(controller, bank, d=1):
    row = attack_access.target_row[bank]
    if attack_access.hammered_time[bank] >= REFRESHCYCLE*2:
        attack_access.target_row[bank] = random.randint(0, controller.get_banksize())
        attack_access.hammered_time[bank] = 0
        if attack_access.target_row[bank] % 2 == 1:
            attack_access.target_row[bank] -= 1

    for i in range(1, (d + 1)):
        controller.read(bank, row - (i))
        controller.read(bank, row + (i))
        attack_access.hammered_time[bank] += 2


attack_access.target_row = [50]*4  # example
attack_access.hammered_time = [0]*4


HELP_MESSAGE = """Usage: test.py <strategy>

Available strategies:
none          - No protection
  para          - PARA protection
  graphene      - Graphene protection
  """

# Mapping strategies to their respective classes simplifies expansion
STRATEGY_MAP = {
    "none": DefaultProtector,
    "para": ParaProtector,
    "graphene": GrapheneProtector,
}


# TODO generate some statistics
def main():
    if len(sys.argv) < 2:
        print(HELP_MESSAGE)
        sys.exit(1)

    strategy = sys.argv[1].lower()

    if strategy not in STRATEGY_MAP:
        print("Unkown strategy: defaulting to None.")
        strategy = "none"

    protector_class = STRATEGY_MAP[strategy]
    protector = protector_class(controller)

    controller.register_protector(protector)

    print("Use the GUI to switch modes")
    while gui.running:
        mode = gui.mode
        sleep_time = gui.sleep_time
        for b in range(4):
            if mode == "normal":
                normal_access(controller, b)
            elif mode == "random":
                random_access(controller, b)
            elif mode == "discover":
                discovery_access(controller, b)
            elif mode == "attack":
                attack_access(controller,b, 1)
        gui.draw()
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
