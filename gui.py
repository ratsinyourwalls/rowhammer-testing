import time
import tkinter as tk


class MemoryGUI:
    def __init__(self, controller, cell_size=20):
        self.controller = controller
        self.cell_size = cell_size
        self.running = True
        self.mode_index = 0
        self.MODES = ["normal", "random", "discover", "attack"]
        self.mode = self.MODES[self.mode_index]
        self._lastcall = 0

        self.row_flipped = [
            [False for _ in range(controller.get_banksize())]
            for _ in range(controller.get_banks())
        ]

        self.row_flash = [
            [0 for _ in range(controller.get_banksize())]
            for _ in range(controller.get_banks())
        ]

        self.root = tk.Tk()
        self.root.title("DRAM RowHammer Simulator")

        width = controller.get_banks() * (cell_size * +4)
        height = controller.get_banksize() * (cell_size + 4)

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        tk.Button(self.root, text="Next mode", command=self.next_mode).pack()
        tk.Button(
            self.root, text="Reset flips", command=self.reset
        ).pack()
        self.mode_label = tk.Label(self.root, text="Mode: normal", font=("Arial", 14))
        self.mode_label.pack()

    def next_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.MODES)
        self.mode = self.MODES[self.mode_index]
        self.mode_label.config(text=f"Mode: {self.mode}")
        print("Switched to mode:", self.mode)

    def close(self):
        self.running = False
        self.root.destroy()

    def notify_flip(self, bank, row):
        self.row_flipped[bank][row] = True

    def reset(self):
        self.controller.memory.reset()
        self.row_flipped = [
            [False for _ in range(self.controller.get_banksize())]
            for _ in range(self.controller.get_banks())
        ]

    def notify_refresh(self, bank):
        pass

    def notify_read(self, bank, row):
        self.row_flash[bank][row] = 3

    def activation_to_color(self, activ):
        max_activ = 100
        t = min(activ / max_activ, 1.0)

        r = int(200 - 150 * t)
        g = int(220 - 180 * t)
        b = int(255 - 200 * t)

        return f"#{r:02x}{g:02x}{b:02x}"

    def draw(self):
        t = time.time_ns()
        if t - self._lastcall >= 1.6e7:
            self._lastcall = t
        else:
            return

        self.canvas.delete("all")

        row_height = 4
        row_spacing = 1
        bank_spacing = 40
        row_width = 300
        left_margin = 20
        top_margin = 20

        banks = self.controller.get_banks()
        rows = self.controller.get_banksize()

        # height of one bank block
        bank_block_height = rows * (row_height + row_spacing)

        # Compute total height needed
        total_width = banks * (row_width + bank_spacing) + left_margin
        total_height = bank_block_height + top_margin + 2

        # Resize canvas dynamically
        self.canvas.config(width=total_width, height=total_height)

        for bank in range(banks):
            # Vertical offset for this bank
            bank_offset_x = left_margin + bank * (row_width + bank_spacing)

            # Label the bank
            self.canvas.create_text(
                bank_offset_x,
                top_margin - 10,
                text=f"Bank {bank}",
                fill="white",
                anchor="w",
            )

            for row in range(rows):
                x = bank_offset_x
                y = top_margin + row * (row_height + row_spacing)

                # Color logic
                flipped = self.row_flipped[bank][row]
                flash = self.row_flash[bank][row]

                if flipped:
                    color = "red"

                else:
                    activ = self.controller.memory.get_ac(bank, row)
                    color = self.activation_to_color(activ)

                self.canvas.create_rectangle(
                    x, y, x + row_width, y + row_height, fill=color, outline=""
                )

        self.root.update()
