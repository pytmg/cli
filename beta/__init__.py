import curses

class Vector2():
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

def get_input(stdscr: curses.window, prompt=""):
    height, width = stdscr.getmaxyx()
    stdscr.refresh()

    WindowHeight, WindowWidth = int(height*0.8), int(width*0.8)

    print((width//2)-(WindowWidth//2), (height//2)-(WindowHeight//2), (height//2) + (WindowHeight//2), (width//2) + (WindowWidth//2))

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
        input_win.addstr(1, 3, f"  {prompt}  ")
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
            continue
        elif 32 <= char <= 126:
            input_str += chr(char)  # Append the character to the input string
            continue

    return input_str

class CLI():
    def __init__(self, title: str = "No title provided"):
        self.title = str(title) if type(title) != str else title
        self.selectedIDX = 0
        self.printStatement = ""
        self.running = False
        self.exitAdded = False
        self.options = []
        self.stdscr = None
        self.ColumnLength = 0
        self.dimensions = 0,0

    def exit(self):
        self.running = False

    def print(self, *args):
        args = [str(arg) for arg in args]
        self.printStatement = "".join(args)

    def input(self, *args):
        return get_input(stdscr=self.stdscr, prompt=" ".join(args))

    def run(self, exitLabel = "Exit", exitDescription = "Exits the program.", exitFunction = None, exitArguments = ()):
        self.addItem(
            name=exitLabel,
            description=exitDescription,
            function=exitFunction or self.exit,
            args=exitArguments,
            keybind="q"
        ) if not self.exitAdded else 0
        self.exitAdded = True
        curses.wrapper(self.main)

    def addItem(self, name: str, description: str, function, args:tuple, keybind: str = None):
        if keybind:
            for option in self.options:
                if keybind == option["key"]:
                    keybind = None
        if not self.exitAdded:
            self.options.append({
                        "name": name,
                        "description": description,
                        "function": function,
                        "args": args,
                        "key": keybind.lower() if keybind else None
                    })
        else:
            EXIT = self.options[-1]
            self.options.pop(-1)
            self.options.append({
                        "name": name,
                        "description": description,
                        "function": function,
                        "args": args,
                        "key": keybind.lower() if keybind else None
                    })
            self.options.append(EXIT)

    def doNothing(self, *args):
        pass

    def main(self, stdscr: curses.window):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()
        stdscr.refresh()

        self.stdscr = stdscr
        self.running = True

        while self.running:
            # Get the current size of the window
            height, width = stdscr.getmaxyx()

            height -= 1
            width -= 2
            stdscr.clear()

            if height > 3 and width > 2:
                for h in range(height):
                    for w in range(width):
                        if h == 0:
                            if w == 0:
                                stdscr.addstr(h, w, "╔")
                            elif 0 < w < width-1:
                                stdscr.addstr(h, w, "═")
                            elif w == width-1:
                                stdscr.addstr(h, w, "╗")
                        elif 0 < h < height-1:
                            if w == 0:
                                stdscr.addstr(h, w, "║")
                            elif w == width-1:
                                stdscr.addstr(h, w, "║")
                        elif h == height-1:
                            if w == 0:
                                stdscr.addstr(h, w, "╚")
                            elif 0 < w < width-1:
                                stdscr.addstr(h, w, "═")
                            elif w == width-1:
                                stdscr.addstr(h, w, "╝")
            
            OptionPosition = Vector2(2, 1)
            DescriptionAreaPosition = Vector2(2, height-11)
            OutputAreaPostition = Vector2(width//2, DescriptionAreaPosition.y)

            TITLE = f"║ {self.title} ║"
            X1 = (width//2) - (len(TITLE)//2)
            X2 = ((width//2) + (len(TITLE)//2)) - (1 if len(TITLE)%2 == 0 else 0)

            self.ColumnLength = height - 16
            self.dimensions = height, width

            stdscr.addstr(0, X1, "╦")
            stdscr.addstr(0, X2, "╦")

            for w in range(X1, X2+1):
                if w == X1:
                    stdscr.addstr(OptionPosition.y+1, w, "╚")
                elif X1 < w < X2:
                    stdscr.addstr(OptionPosition.y+1, w, "═")
                elif w == X2:
                    stdscr.addstr(OptionPosition.y+1, w, "╝")

            for w in range(width):
                if w == 0:
                    stdscr.addstr(DescriptionAreaPosition.y, w, "╠")
                elif 0 < w < width-1:
                    stdscr.addstr(DescriptionAreaPosition.y, w, "═")
                elif w == width-1:
                    stdscr.addstr(DescriptionAreaPosition.y, w, "╣")
            DescriptionAreaPosition.y += 1

            for h in range(OutputAreaPostition.y, height):
                if h == OutputAreaPostition.y:
                    stdscr.addstr(h, OutputAreaPostition.x, "╦")
                elif OutputAreaPostition.y < h < height-1:
                    stdscr.addstr(h, OutputAreaPostition.x, "║")
                elif h == height-1:
                    stdscr.addstr(h, OutputAreaPostition.x, "╩")
            
            stdscr.addstr(OutputAreaPostition.y, OutputAreaPostition.x + 2, " Output ")
            OutputAreaPostition.y += 1
            OutputAreaPostition.x += 2

            for j, Line in enumerate(self.printStatement.split("\n")):
                if len(Line) > (width//2)-3:
                    stdscr.addstr(OutputAreaPostition.y + j, OutputAreaPostition.x, f"{Line[:(width//2)-6]}...")
                else:
                    stdscr.addstr(OutputAreaPostition.y + j, OutputAreaPostition.x, f"{Line}")

            stdscr.addstr(OptionPosition.y, (width//2) - (len(TITLE)//2), TITLE)
            OptionPosition.y += 2

            for i, Option in enumerate(self.options):
                Y_POS = i % self.ColumnLength
                X_MULT = (i // self.ColumnLength) * 25
                if i == self.selectedIDX:
                    stdscr.attron(curses.color_pair(1))
                    if len(Option["name"]) > 20:
                        stdscr.addstr(OptionPosition.y + Y_POS, OptionPosition.x + X_MULT, f"> {Option["name"][:20]}...")
                    else:
                        stdscr.addstr(OptionPosition.y + Y_POS, OptionPosition.x + X_MULT, f"> {Option["name"]}")
                    stdscr.attroff(curses.color_pair(1))
                    stdscr.addstr(DescriptionAreaPosition.y - 1, DescriptionAreaPosition.x, " Description & Keybind " if self.options[self.selectedIDX]["key"] else " Description ")
                    for j, Line in enumerate(self.options[self.selectedIDX]["description"].split("\n")):
                        if len(Line) > (width//2)-3:
                            stdscr.addstr(DescriptionAreaPosition.y + j, DescriptionAreaPosition.x, f"{Line[:(width//2)-6]}...")
                        else:
                            stdscr.addstr(DescriptionAreaPosition.y + j, DescriptionAreaPosition.x, f"{Line}")
                    stdscr.addstr(DescriptionAreaPosition.y + len(self.options[self.selectedIDX]["description"].split("\n")) + 1, DescriptionAreaPosition.x, f"Keybind: {self.options[self.selectedIDX]["key"].upper()}") if self.options[self.selectedIDX]["key"] else 0
                else:
                    if len(Option["name"]) > 15:
                        stdscr.addstr(OptionPosition.y + Y_POS, OptionPosition.x + X_MULT, f"  {Option["name"][:15]}...")
                    else:
                        stdscr.addstr(OptionPosition.y + Y_POS, OptionPosition.x + X_MULT, f"  {Option["name"]}")

            try:
                stdscr.refresh()
                key = stdscr.getch()
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
                    self.options[self.selectedIDX]["function"](*self.options[self.selectedIDX]["args"])
                    self.run() if self.running else 0
                    continue
                else:
                    for option in self.options:
                        try:
                            if key == ord(option["key"]):
                                option["function"](*option["args"])
                                self.run() if self.running else 0
                                continue
                        except:
                            pass
            except KeyboardInterrupt:
                pass