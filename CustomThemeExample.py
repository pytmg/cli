from __init__ import Themes, Borders # use cli instead of __init__ when actually using the framework

class CustomThemes(Themes):
    class SingleStrokeDefault(Themes.Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "Bordered Default Theme"
            self.theme_description = "A default theme with single stroke borders."
            self.theme_author = "tmg"
            self.border = Borders.SingleStroke()

    class CurvedDefault(Themes.Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "Curved Default Theme"
            self.theme_description = "A default theme with curved borders."
            self.theme_author = "tmg"
            self.border = Borders.SingleStroke_Curved()

    class EIR(Themes.Default):
        def __init__(self):
            super().__init__()
            self.theme_name = "/Rx/EVERYTHING IS /rx/RED/Rx/.//"
            self.theme_description = "A fully red theme."
            self.theme_author = "tmg"
            self.border = Borders.Default() # not None

            self.title = "/Rx/[title]//"
            self.defaultOption = "/Rx/  [option]//"
            self.disabledOption = "/rx/  [option]//"
            self.selectedOption = "/Rx/> [option]//"
            self.inp = " /rx/[[val]/rx/]//"
            self.boolean = "/rx/ [x]?OR?/rx/ [ ]"
            self.description = "/Rx/Description\n/Rx/[description]//"
            self.footer = "/Rx/[↑ ↓ enter | [exitkey] = /rx/quit/Rx/] EVERYTHING IS /rx/RED/Rx/."
            self.output = "/Rx/Output//\n/Rx/  [output]//"
            self.arrows = ["/Rx/▲//", "/Rx/▼//"]
            self.UPPERONLY = True