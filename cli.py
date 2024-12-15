try:
    import os
    import keyboard
    import ansi
except ModuleNotFoundError:
    if input("You do not have the required modules to run this.\nInstall now? (Y/n)\n> ").lower().startswith("y"):
        import os
        os.system("pip install ansi keyboard")
        input("Done!\nPress enter to close.")
        exit()
    else:
        exit()

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
            "/b bright_white/": f"{ansi.color.bg.brightwhite}"
        }
        self.print_statement = ""

    def addFunction(self, idx, func, *args):
        """Add a new function to the CLI menu."""
        if not callable(func):
            raise ValueError(f"Argument 'func' must be callable, but got {type(func).__name__}.")
        self.functions[idx] = (func, args)

    def addItem(self, name: str):
        """Add a new item to the CLI menu"""
        try:
            if self.menu_items[-1] == "Exit":
                self.menu_items.pop(-1)
                self.menu_items += [name]
                self.menu_items.append("Exit")
            else:
                self.menu_items += [name]
        except IndexError:
            self.menu_items += [name]

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

    def run(self):
        """Run the CLI interface and handle user input."""
        self.menu_items += ["Exit"]
        self.refresh()

        while True:
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
                        break

                    # Execute custom functions if any
                    if self.selected_index in self.functions:
                        func, args = self.functions[self.selected_index]
                        if args[0] != ():
                            func(*args)
                        else:
                            func()

                    self.refresh()