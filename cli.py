"""
A CLI Menu system module created by TMG.

- Example Usage:

    ```python
    from cli import CLI

    cli = CLI()

    def goodMorning():
        cli.print("Good Morning!")

    cli.addItem("Good morning!", goodMorning, ())

    cli.run()
    ```
"""

DEBUG = False

try:
    import os
    import keyboard
    import ansi
    import random
except ModuleNotFoundError:
    if input("You do not have the required modules to run this.\nInstall now? (Y/n)\n> ").lower().startswith("y"):
        import os
        os.system("pip install ansi keyboard")
        input("Done!\nPress enter to close.")
        exit()
    else:
        exit()

class CLI:
    """
    The main class

    ```py
    cli = CLI(title="Example")
    ```
    """
    def __init__(self, title="No Title Provided"):
        self.running = False
        self.exitMessage = str(random.uniform(-100, 100)) # For complete randomness of the initial Exit - Because of the custom exit message and custom exit function.
        self.title = title
        self.selected_index = 0
        self.menu_items = []
        self.functions = {}
        self.colours = {
            "/f red/": f"{ansi.color.fg.red}",
            "/b red/": f"{ansi.color.bg.red}",
            "/f green/": f"{ansi.color.fg.green}",
            "/b green/": f"{ansi.color.bg.green}",
            "/f yellow/": f"{ansi.color.fg.yellow}",
            "/b yellow/": f"{ansi.color.bg.yellow}",
            "/f blue/": f"{ansi.color.fg.blue}",
            "/b blue/": f"{ansi.color.bg.blue}",
            "/f magenta/": f"{ansi.color.fg.magenta}",
            "/b magenta/": f"{ansi.color.bg.magenta}",
            "/f cyan/": f"{ansi.color.fg.cyan}",
            "/b cyan/": f"{ansi.color.bg.cyan}",
            "/f white/": f"{ansi.color.fg.white}",
            "/b white/": f"{ansi.color.bg.white}",
            "/f black/": f"{ansi.color.fg.black}",
            "/b black/": f"{ansi.color.bg.black}",
            "/f gray/": f"{ansi.color.fg.gray}",
            "/b gray/": f"{ansi.color.bg.gray}",
            "/f bright_red/": f"{ansi.color.fg.brightred}",
            "/b bright_red/": f"{ansi.color.bg.brightred}",
            "/f bright_green/": f"{ansi.color.fg.brightgreen}",
            "/b bright_green/": f"{ansi.color.bg.brightgreen}",
            "/f bright_yellow/": f"{ansi.color.fg.brightyellow}",
            "/b bright_yellow/": f"{ansi.color.bg.brightyellow}",
            "/f bright_blue/": f"{ansi.color.fg.brightblue}",
            "/b bright_blue/": f"{ansi.color.bg.brightblue}",
            "/f bright_magenta/": f"{ansi.color.fg.brightmagenta}",
            "/b bright_magenta/": f"{ansi.color.bg.brightmagenta}",
            "/f bright_cyan/": f"{ansi.color.fg.brightcyan}",
            "/b bright_cyan/": f"{ansi.color.bg.brightcyan}",
            "/f bright_white/": f"{ansi.color.fg.brightwhite}",
            "/b bright_white/": f"{ansi.color.bg.brightwhite}",
            "/e bold/": f"{ansi.color.fx.bold}",
            "/e underline/": f"{ansi.color.fx.underline}",
            "/e italic/": f"{ansi.color.fx.italic}"
        }
        self.print_statement = ""

    def doNothing():
        """Literally does nothing."""
        pass

    def addItem(self, name: str, func, args: tuple = ()):
        """Add a new item to the CLI menu"""
        try:
            if self.menu_items[-1] == self.exitMessage:
                temp = self.menu_items.pop(-1)
                self.menu_items += [name]
                self.menu_items.append(temp)
            else:
                idx = len(self.menu_items)
                if name in self.menu_items:
                    i = 1
                    while True:
                        i += 1
                        if f"{name} ({i})" not in self.menu_items:
                            name = f"{name} ({i})"
                            break
                self.menu_items += [name]
                self.functions[str(idx)] = (func, args)
        except IndexError:
            idx = len(self.menu_items)
            self.menu_items += [name]
            self.functions[str(idx)] = (func, args)

    def print(self, *args, **kwargs):
        """Override the default print to update print statement."""
        self.print_statement = " ".join(args)
        print(*args, **kwargs)

    def refresh(self):
        """Refresh the screen with updated menu."""
        self.cls()
        print(self.title)
        for i, item in enumerate(self.menu_items):
            formatted_item = item
            for color in self.colours:
                formatted_item = formatted_item.replace(color, self.colours[color]).replace("/reset/", f"{ansi.color.bg.white}{ansi.color.fg.black}" if i == self.selected_index else f"{ansi.color.fx.reset}")
            print(f"{f'{ansi.color.bg.white}{ansi.color.fg.black}>' if i == self.selected_index else ' '} {formatted_item}" + f"{ansi.color.fx.reset}")
        print("Use UP and DOWN arrow to navigate, press ENTER to select.")
        print(self.print_statement, end="\r")

    @staticmethod
    def cls():
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def exit(self):
        """Exit the current menu"""
        self.running = False

    def run(self, exitMessage: str = "Exit", exitFunction = None):
        """Run the CLI interface and handle user input."""
        self.exitMessage = exitMessage
        self.running = True
        self.menu_items += [exitMessage]
        self.refresh()

        while self.running:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.scan_code == 80:
                    self.selected_index += 1
                    self.selected_index %= len(self.menu_items)
                    self.refresh()
                elif event.scan_code == 72:
                    self.selected_index -= 1
                    self.selected_index %= len(self.menu_items)
                    self.refresh()
                elif event.scan_code == 28:
                    # Check for the function at the selected index
                    if self.selected_index == len(self.menu_items) - 1:
                        if exitFunction:
                            exitFunction()
                        else:
                            self.exit()

                    # Execute custom functions if any
                    if str(self.selected_index) in self.functions:
                        func, args = self.functions[str(self.selected_index)]
                        func(*args)

                    self.refresh()
            
            print(event.scan_code) if DEBUG else 0
            print(self.selected_index) if DEBUG else 0
            print(self.functions) if DEBUG else 0