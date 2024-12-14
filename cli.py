import os
import keyboard
import ansi

class CLI:
    def __init__(self, title="Test"):
        self.title = title
        self.selected_index = 0
        self.menu_items = []
        self.functions = {}
        self.colours = {
            "/f red/": f"{ansi.color.fg.red}",
            "/b red/": f"{ansi.color.bg.red}",
            "/f green/": f"{ansi.color.fg.green}",
            "/b green/": f"{ansi.color.bg.green}",
        }
        self.print_statement = ""

    def addFunction(self, idx, func, args=()):
        """Add a new function to the CLI menu."""
        self.functions[idx] = (func, args)

    def addItem(self, name: str):
        """Add a new item to the CLI menu"""
        self.menu_items += [name]

    def print(self, *args, **kwargs):
        """Override the default print to update print statement."""
        self.print_statement = " ".join(args)
        __builtins__.print(*args, **kwargs)

    def refresh(self):
        """Refresh the screen with updated menu."""
        self.cls()
        __builtins__.print(self.title)
        for i, item in enumerate(self.menu_items):
            formatted_item = item
            for color in self.colours:
                formatted_item = formatted_item.replace(color, self.colours[color]).replace("/reset/", f"{ansi.color.bg.white}{ansi.color.fg.black}" if i == self.selected_index else f"{ansi.color.fx.reset}")
            __builtins__.print(f"{f'{ansi.color.bg.white}{ansi.color.fg.black}>' if i == self.selected_index else ' '} {formatted_item}" + f"{ansi.color.fx.reset}")
        __builtins__.print("Use UP and DOWN arrow to navigate, press ENTER to select.")
        __builtins__.print(self.print_statement)

    @staticmethod
    def cls():
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        """Run the CLI interface and handle user input."""
        self.menu_items += ["Exit"]
        self.refresh()

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "down":
                    self.selected_index += 1
                    self.selected_index %= len(self.menu_items)
                    self.refresh()
                elif event.name == "up":
                    self.selected_index -= 1
                    self.selected_index %= len(self.menu_items)
                    self.refresh()
                elif event.name == "enter":
                    # Check for the function at the selected index
                    if self.selected_index == len(self.menu_items) - 1:
                        break

                    # Execute custom functions if any
                    if self.selected_index in self.functions:
                        func, args = self.functions[self.selected_index]
                        func(*args)

                    self.refresh()
