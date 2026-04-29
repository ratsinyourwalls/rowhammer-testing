from controller import MemoryController
from protector_template import Protector

controller = MemoryController(1, 1024 * 4, 100)
protector = Protector(controller)
controller.register_protector(protector)


# TODO generate write sequences and pass them to the controller
# TODO generate some statistics
def main():
    pass


if __name__ == "__main__":
    main()
