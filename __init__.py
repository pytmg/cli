"""CLI-V3"""
from typing import Callable, Union, Self
import curses, itertools, os

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
            stdscr.addstr(menu.inset + y, menu.inset + ((x+i)-offset), char.lower() if menu.theme.loweronly else (char.upper() if menu.theme.UPPERONLY else char))
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
    class OPTION:
        def __init__(self, name: str, description: str, action: Callable = None, params: tuple = (), disabled: bool = False, value: Union[bool, None] = None):
            self.name = name
            self.description = description
            self.action = action
            self.params = params
            self.disabled = disabled
            self.value = value

        def act(self):
            return

    class Callable(OPTION):
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
    
    class Boolean(OPTION):
        def __init__(self, name: str, description: str, value: bool = False, disabled: bool = False):
            super().__init__(name=name, description=description, disabled=disabled)
            self.value = value

        def act(self):
            self.value = not self.value

        def __str__(self):
            return self.name
        
        def __dict__(self):
            return {
                "name": self.name,
                "description": self.description,
                "value": self.value
            }
        
        def __call__(self):
            return self.act()

class Borders:
    class Default:
        def __init__(self):
            self.tl = " "
            self.tr = " "
            self.bl = " "
            self.br = " "
            self.h = " "
            self.v = " "
            self.i = " "
            self.td = " "
            self.bu = " "

        @property
        def borders(cls) -> list[str]:
            return [
                cls.tl, cls.tr, cls.bl, cls.br,
                cls.h, cls.v, cls.i, cls.td, cls.bu
            ]

    class SingleStroke(Default):
        def __init__(self):
            super().__init__()
            self.tl = "┌"
            self.tr = "┐"
            self.bl = "└"
            self.br = "┘"
            self.h = "─"
            self.v = "│"
            self.i = "┼"
            self.td = "┬"
            self.bu = "┴"

    class SingleStroke_Curved(Default):
        def __init__(self):
            super().__init__()
            self.tl = "╭"
            self.tr = "╮"
            self.bl = "╰"
            self.br = "╯"
            self.h = "─"
            self.v = "│"
            self.i = "┼"
            self.td = "┬"
            self.bu = "┴"

    class DoubleStroke(Default):
        def __init__(self):
            super().__init__()
            self.tl = "╔"
            self.tr = "╗"
            self.bl = "╚"
            self.br = "╝"
            self.h = "═"
            self.v = "║"
            self.i = "╬"
            self.td = "╦"
            self.bu = "╩"

    @classproperty
    def borderlist(cls) -> list[Default]:
        return [
            member for name, member in vars(cls).items()
            if isinstance(member, type) and issubclass(member, cls.Default)
        ]

class Themes:
    class Default:
        def __init__(self):
            # Set up all combinations of colours
            self.allpairs = "Waiting for init."
            self.border = Borders.Default()
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
            self.boolean = " [x]?OR? [ ]"
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
            if self.allpairs == "Waiting for init.":
                raise RuntimeError("All colours not initialised. Call init() first.")
            return self.allpairs.get((fg, bg), 0)
        
        def init(self):
            self.initcols()

    class V2(Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "CLI-V2 theme"
            self.theme_description = "This theme is inspired by CLI-V2."
            self.border = Borders.DoubleStroke()
            self.selectedOption = "/kw/> [option]"
            self.boolean = " [x]?OR? [ ]"
            self.description = "Description\n  [description]"
            self.output = "Output\n  [output]"
            self.footer = "Use ↑↓ to navigate and press ENTER to select."

    class BlueDefault(Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "Blue Default Theme"
            self.theme_description = "The default theme with blue accents rather than green."
            self.selectedOption = "/Bx/>// [option]"
            self.boolean = " [x]?OR? [ ]"
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
            self.boolean = " [x]?OR? [ ]"
            self.description = "Description\n  [description]"
            self.output = "Output\n  [output]"
            self.footer = "[↑ ↓ enter | q = quit]"

    class MatrixDefault(Default):
        def __init__(self):
            super().__init__()
            self.UPPERONLY = True
            self.title = "/gx/[title]"
            self.theme_name = "Matrix Default Theme"
            self.theme_description = "Green on black theme"
            self.defaultOption = "/gx/  [option]"
            self.selectedOption = "/gx/> [option]"
            self.disabledOption = "/gx/x [option]"
            self.boolean = " [x]?OR? [ ]" # will be appended
            self.description = "/gx/Description\n/gx/  [description]"
            self.output = "/gx/Output\n/gx/  [output]"
            self.arrows = ["/gx/▲", "/gx/▼"]
            self.footer = "/gx/[↑ ↓ enter | q = quit]"

    @classproperty
    def themelist(cls) -> list[Default]:
        return [
            member for name, member in vars(cls).items()
            if isinstance(member, type) and issubclass(member, cls.Default)
        ]

class Menu:
    def __init__(self, title: str, opts: list[Option.OPTION] = None, theme: Themes.Default = Themes.Default(), config: Config = Config()):
        self.stdscr = None
        self.opts = opts or []
        self.config = config
        self.selected = 0
        self.title = title
        self.theme = theme
        self.running = False
        self.printmsg = ""
        self.ScrollOpts = 0
        self.inset = 0
    
    def getOptionByIndex(self, index: int) -> Option.OPTION:
        """
        Get an option by its index.
        """
        if index < len(self.opts):
            return self.opts[index]
        raise IndexError("Option index out of range.")

    def exit(self):
        self.running = False

    def AddOption(self, option: Option.OPTION):
        if isinstance(option, Option.OPTION):
            self.opts.append(option)
        else:
            raise TypeError("Option must be an instance of Option.OPTION class")
        
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

        H_, W_ = stdscr.getmaxyx()
        W_ -= 1
        h, w = H_, W_

        if any([border != " " for border in self.theme.border.borders]):
            self.inset = 2
        else:
            self.inset = 0

        h -= self.inset * 2
        w -= self.inset * 2

        while self.running:
            stdscr.clear()
            if self.inset != 0:
                # -- DRAW BORDERS -- 
                border = self.theme.border
                stdscr.addch(0, 0, border.tl)
                stdscr.addch(0, W_ - 1, border.tr)
                stdscr.addch(H_ - 1, 0, border.bl)
                stdscr.addch(H_ - 1, W_ - 1, border.br)

                for i in range(1, W_ - 1):
                    stdscr.addch(0, i, border.h)
                    stdscr.addch(H_ - 1, i, border.h)
                for i in range(1, H_ - 1):
                    stdscr.addch(i, 0, border.v)
                    stdscr.addch(i, W_ - 1, border.v)

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
                OptionNameValue = str(option)
                if isinstance(option, Option.Boolean):
                    OptionNameValue += self.theme.boolean.split("?OR?")[0 if option.value else 1]

                if option.disabled:
                    string = self.theme.disabledOption.replace("[option]", OptionNameValue)
                else:
                    string = self.theme.selectedOption.replace("[option]", OptionNameValue) if j == self.selected else self.theme.defaultOption.replace("[option]", OptionNameValue)

                if len(string) > w - 2:
                    string = string[:w - 2]

                Utility.addstr(self, 1 + i, 0, string)

            if self.ScrollOpts > 0:
                Utility.addstr(self, 1, 0 if (stdscr.inch(1+self.inset, 0+self.inset) & 0xFF) == ord(' ') else 1, self.theme.arrows[0])

            if self.ScrollOpts + max_visible < len(self.opts):
                Utility.addstr(self, max_visible, 0 if (stdscr.inch(max_visible+self.inset, 0+self.inset) & 0xFF) == ord(' ') else 1, self.theme.arrows[1])

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

            Utility.addstr(self, h - 1, 0, (self.theme.footer + (f"// Theme by: {self.theme.theme_author}//" if self.theme.theme_author != "__builtin__" else ""))[:w-1])

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

                    try:
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
                    except:
                        continue
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
                H_, W_ = stdscr.getmaxyx()
                W_ -= 1
                h, w = H_, W_
                h -= self.inset * 2
                w -= self.inset * 2
                stdscr.clear()
                stdscr.refresh()
            elif ky == ord('q'):
                self.exit()
                curses.nocbreak()
                curses.echo()
                stdscr.keypad(False)

    def run(self):
        try:
            self.running = True
            curses.wrapper(self._main)
        except Exception as e:
            if os.name == "nt":
                curses.endwin()
            raise e
        finally:
            if self.stdscr:
                if os.name == "nt":
                    curses.endwin()
    
    def __call__(self, *args, **kwargs):
        """
        Run the menu.
        """
        self.run(*args, **kwargs)