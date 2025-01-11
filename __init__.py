"""CLI-V2

- Authors:
    - [pytmg](https://github.com/pytmg)

- Example Usage:

    ```python
    from cli import CLI, Option

    cli = CLI()

    def goodMorning():
        cli.print("Good Morning!")

    cli.addItem(Option.Default("Good morning!", "Say \\"Good Morning\\"", goodMorning, ()))

    cli.run()
    ```"""

import curses

class Vector2():
    """A 2D Vector"""
    def __init__(self, x: int = 0, y: int = 0):
        """Create a new Vector2"""
        self.x = x
        self.y = y

def is_iterable(obj):
    return hasattr(obj, '__iter__')

def get_input(stdscr: curses.window, prompt:str="", numOnly: bool = False):
    height, width = stdscr.getmaxyx()
    stdscr.refresh()
    stdscr.keypad(True)

    WindowHeight, WindowWidth = int(height*0.8), int(width*0.8)

    # Create a window to take input
    input_win = curses.newwin(WindowHeight, WindowWidth, (height // 2) - (WindowHeight // 2), (width // 2) - (WindowWidth // 2))
    input_win_win = curses.newwin(WindowHeight-3, WindowWidth-6, (height // 2) - (WindowHeight // 2) + 2, (width // 2) - (WindowWidth // 2)+3)
    # Store the input string
    input_str = ''
    
    while True:
        input_win.clear()
        if WindowHeight > 3 and WindowWidth > 2:
            for h in range(WindowHeight):
                for w in range(WindowWidth):
                    if h == 1:
                        if w == 1:
                            input_win.addstr(h, w, "╔")
                        elif 1 < w < WindowWidth - 2:
                            input_win.addstr(h, w, "═")
                        elif w == WindowWidth - 2:
                            input_win.addstr(h, w, "╗")
                    elif 1 < h < WindowHeight - 1:
                        if w == 1:
                            input_win.addstr(h, w, "║")
                        elif w == WindowWidth - 2:
                            input_win.addstr(h, w, "║")
                    elif h == WindowHeight - 1:
                        if w == 1:
                            input_win.addstr(h, w, "╚")
                        elif 1 < w < WindowWidth - 2:
                            input_win.addstr(h, w, "═")
                        elif w == WindowWidth - 2:
                            input_win.addstr(h, w, "╝")
        if len(prompt) <= WindowWidth - 5:
            input_win.addstr(1, 3, f"  {prompt}  ")
        else:
            input_win.addstr(1, 3, f"  {prompt[:WindowWidth-5]}...  ")
        input_win.refresh()
        input_win_win.clear()
        Area = (WindowHeight-3) * (WindowWidth-6) - 1
        if len(input_str) >= Area:
            input_str = input_str[:Area]
        input_win_win.addstr(0, 0, input_str + " ")
        input_win_win.refresh()
        char = input_win_win.getch()
        
        if char == 10:  # Enter key (newline)
            break
        elif char == 27:  # Escape key
            return None
        elif char == 263 or char == 127 or char == 8:  # Backspace
            input_str = input_str[:-1]
        elif (numOnly and (char in range(48, 58) or char in range(96, 106))) or (not numOnly and 32 <= char <= 126):
            if numOnly:
                input_str += chr(char if char < 96 else char - 48)  # Convert keypad numbers to number row
            else:
                input_str += chr(char)
                continue

    return input_str if not numOnly else int(input_str)

class Config:
    """Configuration for CLI"""
    def __init__(self, *, ShowOutput: bool = True, ShowDescription: bool = True, ShowTitle: bool = True, AutoScale: bool = True):
        self.showout = ShowOutput
        self.showdesc = ShowDescription
        self.title = ShowTitle
        self.scale = AutoScale

class Border:
    """CLI Border"""
    def __init__(self, *, Type: str = "Double"):
        self.types = ["Double", "Single"]
        if Type not in self.types:
            print("Invalid Type, using default..")
            Type = "Double"
        Type = self.types.index(Type)
        self.topLeft = "╔┌"[Type]
        self.topRight = "╗┐"[Type]
        self.bottomLeft = "╚└"[Type]
        self.bottomRight = "╝┘"[Type]
        self.horizontal = "═─"[Type]
        self.vertical = "║│"[Type]
        self.rightToLeft = "╣┤"[Type]
        self.leftToRight = "╠├"[Type]
        self.topToBottom = "╦┬"[Type]
        self.bottomToTop = "╩┴"[Type]
        self.intersection = "╬┼"[Type]

class Option:
    """Options for the CLI"""
    class Base():
        """Base class for options. - Only use this for type hints."""
        def __init__(self):
            self.name = ""
            self.description = ""
            self.keybind = None
            self.args = ()
            self.function = CLI.doNothing
            self.value = None

        def INTERACTION(self, *, stdscr: curses.window):
            pass

    class Default(Base):
        """Runs a function when selected"""
        def __init__(self, name, description, function, args = (), keybind = None):
            self.name = name
            self.description = description
            self.function = function
            self.args = args
            self.keybind = keybind

        def INTERACTION(self, *, stdscr: curses.window):
            self.function(*self.args) if is_iterable(self.args) else self.function(self.args)
            
    class Boolean(Base):
        """Boolean (On/Off)"""
        def __init__(self, name, description, default = False, keybind = None):
            self.name = name
            self.description = description
            self.value = default
            self.default = default
            self.keybind = keybind

        def INTERACTION(self, *, stdscr: curses.window):
            self.value = not self.value

    class Input(Base):
        class Base():
            """Base class for input options."""
            pass

        class String(Base):
            """String input"""
            def __init__(self, name, description, default = "", keybind = None):
                self.name = name
                self.description = description
                self.value = default
                self.default = default
                self.keybind = keybind

            def INTERACTION(self, *, stdscr: curses.window):
                self.value = get_input(stdscr=stdscr, prompt=self.name)

        class Number(Base):
            """Number input"""
            def __init__(self, name, description, default = 0, keybind = None):
                self.name = name
                self.description = description
                self.value = default
                self.default = default
                self.keybind = keybind
            
            def INTERACTION(self, *, stdscr: curses.window):
                self.value = get_input(stdscr=stdscr, prompt=self.name, numOnly=True)

class CLI():
    """The CLI
    
    Usage:
    ```python
    from cli import CLI, Option

    cli = CLI("YourTitleHere")
    idx = cli.addItem(
        Option.Default(
            name="Hello World",
            description="Prints 'Hello, World!'",
            function=cli.print,
            args=("Hello, World!",)
        )
    )
    cli.run()
    """
    def __init__(self, title: str = "No title provided", config: Config = Config(), borders: Border = Border()):
        """Create a new CLI
        
        Params:
            title: str - The title of the CLI"""
        self.title = str(title) if type(title) != str else title
        self.selectedIDX = 0
        self.printStatement = ""
        self.running = False
        self.exitAdded = False
        self.options = []
        self.stdscr = None
        self.ColumnLength = 0
        self.dimensions = 0,0
        self.config = config
        self.border = borders
        self.initial = Vector2()

    def exit(self):
        """Exit the CLI"""
        self.running = False

    def print(self, *args) -> None:
        """Print a statement to the output area
        
        Params:
            *args: str - The statement to print
            
        Returns:
            None"""
        args = [str(arg) for arg in args]
        self.printStatement = "".join(args)

    def input(self, *args) -> str:
        """Get input from the user

        Params:
            *args: str - The prompt to display to the user
            
        Returns:
            str - The input from the user"""
        return get_input(stdscr=self.stdscr, prompt=" ".join(args))

    def run(self, exitLabel = "Exit", exitDescription = "Exits the program.", exitFunction = None, exitArguments = ()) -> None:
        """Run the CLI

        Params:
            exitLabel: str - The name of the exit option
            exitDescription: str - The description of the exit option
            exitFunction: function - The function to run when the exit option is selected
            exitArguments: tuple - The arguments to pass to the exit function"""
        self.addItem(Option.Default(
            name=exitLabel,
            description=exitDescription,
            function=exitFunction or self.exit,
            args=exitArguments,
            keybind="q"
        )) if not self.exitAdded else 0
        self.exitAdded = True
        curses.wrapper(self.main)

    def addItem(self, option: Option.Base) -> int:
        """Add an option to the menu

        Params:
            option: Option.Base - Any type of option to add to the menu
            
        Returns:
            int - The index of the option in the options list"""
        temp = option.name
        
        NAMES = []

        for opt in self.options:
            NAMES.append(opt.name[:])

        if temp in NAMES:
            number = 1
            while True:
                number += 1
                if f"{temp} ({number})" not in NAMES:
                    temp = f"{temp} ({number})"
                    break
            option.name = temp

        # Handle keybinding conflict
        if option.keybind:
            for option2 in self.options:
                if option.keybind == option2.keybind:
                    option.keybind = None
                    break

        # Add the option to the list
        if not self.exitAdded:
            idx = len(self.options)
            self.options.append(option)
        else:
            exit_option = self.options.pop()
            idx = len(self.options)
            self.options.append(option)
            self.options.append(exit_option)
        
        return idx


    def getValueByIndex(self, index):
        """Get the value of an option at a specific index

        Params:
            index: int - The index of the option to get the value of
        """
        if isinstance(self.options[index], Option.Default):
            raise AttributeError("Type 'Option.Default' has no attribute 'value'")
        return self.options[index].value

    def getValueByName(self, name):
        """Get the value of an option by its name

        Params:
            name: str - The name of the option to get the value of
        """
        for option in self.options:
            if option.name == name:
                if isinstance(option, Option.Default):
                    raise AttributeError("Type 'Option.Default' has no attribute 'value'")
                return option.value
        raise ValueError(f"No option found with the name '{name}'")

    def doNothing(self, *args):
        """Frankly, does absolutely nothing."""
        pass

    def main(self, stdscr: curses.window):
        """Literally the backbone of the entire CLI."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selected Colours
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        stdscr.timeout(1000) # 1s timeout, so if anything updates, you dont have to do anything.

        self.stdscr = stdscr
        self.running = True
        height, width = stdscr.getmaxyx()
        if self.initial.x == 0 and self.initial.y == 0:
            self.initial = Vector2(width, height)

        while self.running: # Main loop
            if self.config.scale:
                height, width = stdscr.getmaxyx()
            else:
                height, width = self.initial.y, self.initial.x
            try:
                height -= 1
                width -= 2
                stdscr.clear()

                if height > 3 and width > 2:
                    for h in range(height):
                        for w in range(width):
                            if h == 0:
                                if w == 0:
                                    stdscr.addstr(h, w, self.border.topLeft)
                                elif 0 < w < width-1:
                                    stdscr.addstr(h, w, self.border.horizontal)
                                elif w == width-1:
                                    stdscr.addstr(h, w, self.border.topRight)
                            elif 0 < h < height-1:
                                if w == 0 or w == width-1:
                                    stdscr.addstr(h, w, self.border.vertical)
                            elif h == height-1:
                                if w == 0:
                                    stdscr.addstr(h, w, self.border.bottomLeft)
                                elif 0 < w < width-1:
                                    stdscr.addstr(h, w, self.border.horizontal)
                                elif w == width-1:
                                    stdscr.addstr(h, w, self.border.bottomRight)
                
                OptionPosition = Vector2(2, 1)
                DescriptionAreaPosition = Vector2(2, height-11)
                OutputAreaPostition = Vector2((width//2) if self.config.showdesc else 2, DescriptionAreaPosition.y)

                TITLE = f"{self.border.vertical} {self.title} {self.border.vertical}" if self.config.title else ""
                X1 = (width//2) - (len(TITLE)//2)
                X2 = ((width//2) + (len(TITLE)//2)) - (1 if len(TITLE)%2 == 0 else 0)

                self.ColumnLength = height - (17 if self.config.showdesc or self.config.showout else 6)
                self.dimensions = height, width
                stdscr.addstr((DescriptionAreaPosition.y-2) if self.config.showdesc or self.config.showout else height-2, DescriptionAreaPosition.x, "Use ↑↓←→ to navigate and press ENTER to select.")

                stdscr.addstr(0, X1, self.border.topToBottom) if self.config.title else 0
                stdscr.addstr(0, X2, self.border.topToBottom) if self.config.title else 0

                for w in range(X1, X2+1):
                    if w == X1:
                        stdscr.addstr(OptionPosition.y+1, w, self.border.bottomLeft)
                    elif X1 < w < X2:
                        stdscr.addstr(OptionPosition.y+1, w, self.border.horizontal)
                    elif w == X2:
                        stdscr.addstr(OptionPosition.y+1, w, self.border.bottomRight)

                if self.config.showdesc or self.config.showout:
                    for w in range(width):
                        if w == 0:
                            stdscr.addstr(DescriptionAreaPosition.y, w, self.border.leftToRight)
                        elif 0 < w < width-1:
                            stdscr.addstr(DescriptionAreaPosition.y, w, self.border.horizontal)
                        elif w == width-1:
                            stdscr.addstr(DescriptionAreaPosition.y, w, self.border.rightToLeft)
                    DescriptionAreaPosition.y += 1

                if self.config.showdesc and self.config.showout:
                    for h in range(OutputAreaPostition.y, height):
                        if h == OutputAreaPostition.y:
                            stdscr.addstr(h, OutputAreaPostition.x, self.border.topToBottom)
                        elif OutputAreaPostition.y < h < height-1:
                            stdscr.addstr(h, OutputAreaPostition.x, self.border.vertical)
                        elif h == height-1:
                            stdscr.addstr(h, OutputAreaPostition.x, self.border.bottomToTop)
                
                stdscr.addstr(OutputAreaPostition.y, OutputAreaPostition.x + (2 if self.config.showdesc else 0), " Output ") if self.config.showout else 1
                OutputAreaPostition.y += 1
                OutputAreaPostition.x += 2 if self.config.showdesc else 0

                if self.config.showout:
                    for j, Line in enumerate(self.printStatement.split("\n")):
                        if len(Line) > (width//2)-3:
                            stdscr.addstr(OutputAreaPostition.y + j, OutputAreaPostition.x, f"{Line[:(width//2)-6]}...")
                        else:
                            stdscr.addstr(OutputAreaPostition.y + j, OutputAreaPostition.x, f"{Line}")

                stdscr.addstr(OptionPosition.y, (width//2) - (len(TITLE)//2), TITLE)
                OptionPosition.y += 2 if self.config.title else 1

                def render_option(option, Y_POS, X_MULT, max_len=20, isActive = False):
                    display_name = option.name if len(option.name) <= max_len else option.name[:max_len] + "..."
                    if isinstance(option, Option.Boolean):
                        display_value = f" {'[x]' if option.value else '[ ]'}"
                    else:
                        display_value = ""
                    if isActive:
                        Status = ">"
                    else:
                        Status = " "
                    return f"{Status} {display_name}{display_value}"

                def render_description(stdscr, option, width):
                    description_lines = option.description.split("\n")
                    for j, line in enumerate(description_lines):
                        if len(line) > (width//2)-3:
                            stdscr.addstr(DescriptionAreaPosition.y + j, DescriptionAreaPosition.x, f"{line[:(width//2)-6]}...")
                        else:
                            stdscr.addstr(DescriptionAreaPosition.y + j, DescriptionAreaPosition.x, f"{line}")
                    if option.keybind:
                        stdscr.addstr(DescriptionAreaPosition.y + len(description_lines) + 1, DescriptionAreaPosition.x, f"Keybind: {option.keybind.upper()}")

                for i, option in enumerate(self.options):
                    Y_POS = i % self.ColumnLength
                    X_MULT = (i // self.ColumnLength) * 25

                    # Call render_option to render the option text
                    isActive = i == self.selectedIDX
                    stdscr.attron(curses.color_pair(1)) if isActive else 0
                    stdscr.addstr(OptionPosition.y + Y_POS, OptionPosition.x + X_MULT, render_option(option, Y_POS, X_MULT, isActive=isActive))
                    stdscr.attroff(curses.color_pair(1)) if isActive else 0

                    if isActive and self.config.showdesc:
                        stdscr.addstr(DescriptionAreaPosition.y - 1, DescriptionAreaPosition.x, " Description & Keybind " if option.keybind else " Description ")
                        render_description(stdscr, option, width)

                try:
                    stdscr.refresh()
                    key = stdscr.getch()
                    if key == -1: # when timeout finishes
                        continue
                    if key == curses.KEY_RESIZE:
                        continue
                    elif key == curses.KEY_UP:
                        self.selectedIDX -= 1
                        self.selectedIDX %= len(self.options)
                        continue
                    elif key == curses.KEY_DOWN:
                        self.selectedIDX += 1
                        self.selectedIDX %= len(self.options)
                        continue
                    elif key == curses.KEY_RIGHT:
                        self.selectedIDX += self.ColumnLength
                        if self.selectedIDX > len(self.options):
                            self.selectedIDX = len(self.options)-1
                        continue
                    elif key == curses.KEY_LEFT:
                        self.selectedIDX -= self.ColumnLength
                        if self.selectedIDX < 0:
                            self.selectedIDX = 0
                        continue
                    elif key == 10:
                        self.options[self.selectedIDX].INTERACTION(stdscr=self.stdscr)
                        self.run() if self.running else 0
                        continue
                    else:
                        for option in self.options:
                            try:
                                if key == ord(option.keybind):
                                    option.INTERACTION(stdscr=self.stdscr)
                                    self.run() if self.running else 0
                                    continue
                            except:
                                pass
                except KeyboardInterrupt:
                    pass
            except curses.error as e:
                if not str(e).startswith("addwstr()"):
                    break
                try:
                    stdscr.clear()
                    pos = Vector2(width//2, height//2)
                    text = "Too Small!"
                    stdscr.addstr(pos.y, pos.x - (len(text)//2), text)
                    stdscr.refresh()
                    stdscr.getch()
                except curses.error:
                    stdscr.clear()
                    stdscr.addstr(0,0, "Too Small!")
                    stdscr.refresh()
                    stdscr.getch()