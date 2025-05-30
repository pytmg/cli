"""CLI-V3"""
from typing import Callable, Union
import curses, itertools

class classproperty(property):
    def __get__(self, obj, objtype=None):
        return self.fget(objtype)

class Config:
    def __init__(self, UseMouse: bool = True):
        self.Mouse = UseMouse

class Utility:
    class Colour:
        def __init__(self, fg: int, bg: int):
            self.fg = fg
            self.bg = bg

        def AttrON(self, menu):
            """
            Apply color attr
            """
            theme = menu.theme
            menu.stdscr.attron(curses.color_pair(theme.GetPair(self.fg, self.bg)))

        def AttrOFF(self, menu):
            """
            Remove color attr
            """
            theme = menu.theme
            menu.stdscr.attroff(curses.color_pair(theme.GetPair(self.fg, self.bg)))

    @staticmethod
    def addstr(menu, y: int, x: int, string: str):
        stdscr = menu.stdscr
        offset = 0
        changingCol = False
        currentColor = Utility.Colour(curses.COLOR_WHITE, curses.COLOR_BLACK)
        isBG = None
        ignoreNext = False
        for i, char in enumerate(string):
            if not ignoreNext:
                if char == "\\":
                    offset += 1
                    ignoreNext = True
                    continue
                if char == "/":
                    offset += 1
                    if changingCol:
                        changingCol = False
                        if (isBG == False): # cuz isBG can be None, so we wanna be exact
                            currentColor.AttrOFF(menu)
                            currentColor = Utility.Colour(curses.COLOR_WHITE, curses.COLOR_BLACK)
                    else:
                        changingCol = True
                        isBG = False
                    continue
                if changingCol:
                    offset += 1
                    cols = {
                        'g': curses.COLOR_GREEN,
                        'G': 10,  # Bright Green
                        'b': curses.COLOR_BLUE,
                        'B': 9,  # Bright Blue
                        'r': curses.COLOR_RED,
                        'R': 12,  # Bright Red
                        'y': curses.COLOR_YELLOW,
                        'Y': 14,  # Bright Yellow
                        'w': curses.COLOR_WHITE,
                        'm': curses.COLOR_MAGENTA,
                        'M': 13,  # Bright Magenta
                        'c': curses.COLOR_CYAN,
                        'C': 11,  # Bright Cyan
                        'k': curses.COLOR_BLACK,
                        'z': 8,
                        'x': "x"
                    }
                    if char in cols:
                        if isBG == False:
                            if char != "x":
                                currentColor.fg = cols[char]
                            isBG = True
                        elif isBG == True:
                            if char != "x":
                                currentColor.bg = cols[char]
                            isBG = None
                    elif char == "/":
                        if isBG is False:
                            currentColor.AttrOFF(menu)
                        currentColor = Utility.Colour(curses.COLOR_WHITE, curses.COLOR_BLACK)
                        changingCol = False
                        isBG = None
                    else:
                        continue
                    continue
                ignoreNext = False
            currentColor.AttrON(menu)
            stdscr.addstr(y, (x+i)-offset, char.lower() if menu.theme.loweronly else (char.upper() if menu.theme.UPPERONLY else char))
            currentColor.AttrOFF(menu)

    @staticmethod
    def InitAllColourPairs():
        curses.start_color()
        colors = [
            curses.COLOR_GREEN,
            10,  # Bright Green
            curses.COLOR_BLUE,
            9,  # Bright Blue
            curses.COLOR_RED,
            12,  # Bright Red
            curses.COLOR_YELLOW,
            14,  # Bright Yellow
            curses.COLOR_WHITE,
            curses.COLOR_MAGENTA,
            13,  # Bright Magenta
            curses.COLOR_CYAN,
            11,  # Bright Cyan
            curses.COLOR_BLACK,
            8
        ]
        
        pair_mapping = {}
        pair_number = 1  # pair 0 is reserved, start from 1
        
        for fg, bg in itertools.product(colors, repeat=2):
            curses.init_pair(pair_number, fg, bg)
            pair_mapping[(fg, bg)] = pair_number
            pair_number += 1
        
        return pair_mapping

class Option:
    def __init__(self, name: str, description: str, action: Callable = None, params: tuple = (), disabled: bool = False):
        self.name = name
        self.description = description
        self.action = action
        self.params = params
        self.disabled = disabled

    def act(self):
        if callable(self.action):
            self.action(*self.params)

    def __str__(self):
        return self.name
    
    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description
        }
    
    def __call__(self):
        return self.act()

class Themes:
    class Default:
        def __init__(self):
            # Set up all combinations of colours
            self.allpairs = "Waiting for start."
            self.border = []
            self.theme_name = "Default Theme"
            self.theme_author = "__builtin__"
            self.theme_description = "This is the default theme. Uses standard colors and styles."
            # colour codes
            #  /FB/ Foreground Background
            #   g for green
            #   G for bright green
            #   b for blue
            #   B for bright blue
            #   r for red
            #   R for bright red
            #   y for yellow
            #   Y for bright yellow
            #   w for white
            #   m for magenta
            #   M for bright magenta
            #   c for cyan
            #   C for bright cyan
            #   k for black
            #   z for gray
            #   x for no change
            #  // Reset
            self.title = "[title]"
            self.defaultOption = "  [option]"
            self.disabledOption = "  /zx/[option]//"
            self.selectedOption = "/gx/>// [option]"
            self.description = "Description\n  /gx/[description]"
            self.footer = "[↑ ↓ enter | q = /gx/quit//]"
            self.output = "Output\n  /gx/[output]"
            self.arrows = ["▲", "▼"]
            self._loweronly = False
            self._UPPERONLY = False

        @property
        def loweronly(self) -> bool:
            return self._loweronly
        
        @loweronly.setter
        def loweronly(self, value: bool):
            if not isinstance(value, bool):
                raise TypeError("loweronly must be a boolean value.")
            self._loweronly = value
            if self._UPPERONLY:
                self._UPPERONLY = not value

        @property
        def UPPERONLY(self) -> bool:
            return self._UPPERONLY
        
        @UPPERONLY.setter
        def UPPERONLY(self, value: bool):
            if not isinstance(value, bool):
                raise TypeError("UPPERONLY must be a boolean value.")
            self._UPPERONLY = value
            if self._loweronly:
                self._loweronly = not value

        def initcols(self):
            self.allpairs = Utility.InitAllColourPairs()

        def GetPair(self, fg: int, bg: int) -> int:
            """
            Get the color pair number for the given foreground and background colors.
            """
            if self.allpairs == "Waiting for start.":
                raise RuntimeError("All colours not initialised. Call init() first.")
            return self.allpairs.get((fg, bg), 0)
        
        def init(self):
            self.initcols()

    class BlueDefault(Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "Blue Default Theme"
            self.theme_description = "The default theme with blue accents rather than green."
            self.selectedOption = "/Bx/>// [option]"
            self.description = "Description\n  /Bx/[description]"
            self.output = "Output\n  /Bx/[output]"
            self.footer = "[↑ ↓ enter | q = /Bx/quit//]"

    class Colourless(Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "Colourless Default Theme"
            self.theme_description = "The default theme without colours"
            self.selectedOption = "> [option]"
            self.disabledOption = "x [option]"
            self.description = "Description\n  [description]"
            self.output = "Output\n  [output]"
            self.footer = "[↑ ↓ enter | q = quit]"

    @classproperty
    def themelist(cls) -> list[type]:
        return [
            member for name, member in vars(cls).items()
            if isinstance(member, type) and issubclass(member, cls.Default)
        ]

class Menu:
    def __init__(self, title: str, opts: list[Option] = None, theme: Themes.Default = Themes.Default(), config: Config = Config()):
        self.stdscr = None
        self.opts = opts or []
        self.config = config
        self.selected = 0
        self.title = title
        self.theme = theme
        self.running = False
        self.printmsg = ""
        self.ScrollOpts = 0
    
    def exit(self):
        self.running = False

    def AddOption(self, option: Option):
        if isinstance(option, Option):
            self.opts.append(option)
        else:
            raise TypeError("Option must be an instance of Option class")
        
    def print(self, *text: str, sep: str = " ", end:str="\n", CLEAR: bool = True):
        if CLEAR:
            self.printmsg = sep.join([str(thing) for thing in text]) + end
        else:
            self.printmsg += sep.join([str(thing) for thing in text]) + end

    def _main(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.theme.init()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()

        h, w = stdscr.getmaxyx()

        while self.running:
            stdscr.clear()
            Utility.addstr(self, 0, 0, self.theme.title.replace("[title]", self.title))

            # -- OPTION DISPLAY --
            visible_lines = h - 3
            max_visible = min(len(self.opts), visible_lines)

            if self.selected < self.ScrollOpts:
                self.ScrollOpts = self.selected
            elif self.selected >= self.ScrollOpts + max_visible:
                self.ScrollOpts = self.selected - max_visible + 1

            self.ScrollOpts = max(0, min(self.ScrollOpts, max(0, len(self.opts) - max_visible)))

            for i in range(max_visible):
                j = self.ScrollOpts + i
                if j >= len(self.opts):
                    break

                option = self.opts[j]

                if option.disabled:
                    string = self.theme.disabledOption.replace("[option]", str(option))
                else:
                    string = self.theme.selectedOption.replace("[option]", str(option)) if j == self.selected else self.theme.defaultOption.replace("[option]", str(option))

                if len(string) > w - 2:
                    string = string[:w - 2]

                Utility.addstr(self, 1 + i, 0, string)

            if self.ScrollOpts > 0:
                Utility.addstr(self, 1, 0 if (stdscr.inch(1, 0) & 0xFF) == ord(' ') else 1, self.theme.arrows[0])

            if self.ScrollOpts + max_visible < len(self.opts):
                Utility.addstr(self, max_visible, 0 if (stdscr.inch(max_visible, 0) & 0xFF) == ord(' ') else 1, self.theme.arrows[1])

            # -- DESCRIPTION DISPLAY --
            desc = self.opts[self.selected].description if self.opts else "No options available."
            desc_y = 2 + len(self.opts)
            desc_x = 0
            if desc_y >= h - len(desc.split("\n")) - 2:
                desc_y = 0
                desc_x = w // 2
            string = "\n".join([line[:(w-desc_x)-1] for line in self.theme.description.split("\n")][:-1])
            Utility.addstr(self, desc_y, desc_x, string)
            desc_lines = desc.split("\n")
            for i, line in enumerate(desc_lines):
                if desc_y + 1 + i < (h - 2 ):
                    Utility.addstr(self, desc_y + 1 + i, desc_x, self.theme.description.split("\n")[-1].replace("[description]", line)[:(w-desc_x)-1])

            Utility.addstr(self, stdscr.getmaxyx()[0] - 1, 0, (self.theme.footer + (f"// Theme by: {self.theme.theme_author}//" if self.theme.theme_author != "__builtin__" else ""))[:w-1])

            # -- OUTPUT DISPLAY --
            outp = self.printmsg
            outp_y = 0
            outp_x = w // 2
            if desc_x != 0:
                outp_y = len(self.theme.description.replace("[description]", desc).split("\n")) + 1
            string = "\n".join([line[:(w-outp_x)-1] for line in self.theme.output.split("\n")][:-1])
            printable = True
            try:
                Utility.addstr(self, outp_y, outp_x, string)
            except:
                printable = False
            if printable:
                outp_lines = outp.split("\n")
                for i, line in enumerate(outp_lines):
                    if outp_y + 1 + i < h - 2:
                        Utility.addstr(self, outp_y + 1 + i, outp_x, self.theme.output.split("\n")[-1].replace("[output]", line)[:(w-outp_x)-1])

            # -- KEYBOARD AND MOUSE HANDLERS --
            ky = stdscr.getch()
            
            # -- MOUSE --
            if self.config.Mouse:
                if ky == curses.KEY_MOUSE:
                    _, x, y, _, bstate = curses.getmouse()

                    if bstate & curses.BUTTON1_CLICKED:
                        if self.opts:
                            if not self.opts[self.selected].disabled:
                                self.opts[self.selected].act()
                                self.run() if self.running else 0
                    elif bstate & curses.BUTTON4_PRESSED:
                        self.selected = (self.selected - 1) % len(self.opts)
                        while self.opts[self.selected].disabled and len(self.opts) > 1:
                            self.selected = (self.selected - 1) % len(self.opts)
                    elif bstate & curses.BUTTON5_PRESSED:
                        self.selected = (self.selected + 1) % len(self.opts)
                        while self.opts[self.selected].disabled and len(self.opts) > 1:
                            self.selected = (self.selected + 1) % len(self.opts)
                    continue

            # -- KEYBOARD --
            if ky in [curses.KEY_UP, 450]:
                self.selected = (self.selected - 1) % len(self.opts)
                while self.opts[self.selected].disabled and len(self.opts) > 1:
                    self.selected = (self.selected - 1) % len(self.opts)
            elif ky in [curses.KEY_DOWN, 456]:
                self.selected = (self.selected + 1) % len(self.opts)
                while self.opts[self.selected].disabled and len(self.opts) > 1:
                    self.selected = (self.selected + 1) % len(self.opts)
            elif ky == ord('\n'):
                if self.opts:
                    if not self.opts[self.selected].disabled:
                        self.opts[self.selected].act()
                        self.run() if self.running else 0
            elif ky == curses.KEY_RESIZE:
                h, w = stdscr.getmaxyx()
                stdscr.clear()
                stdscr.refresh()
            elif ky == ord('q'):
                self.running = False

    def run(self):
        try:
            self.running = True
            curses.wrapper(self._main)
        except Exception as e:
            curses.endwin()
            raise e
        finally:
            if self.stdscr:
                curses.endwin()
    
    def __call__(self, *args, **kwargs):
        """
        Run the menu.
        """
        self.run(*args, **kwargs)