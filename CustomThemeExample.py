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