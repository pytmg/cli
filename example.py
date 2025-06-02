# Example script for CLI-V3beta1

from __init__ import Menu, Option, Themes # dont use __init__ when you're actually using the framework, use "cli"

menu = Menu("Wow!")

selectedTheme = 0

def ThemeChanger():
    submenu = Menu("Theme Changer", theme=menu.theme)

    def ChangeTheme(theme: Themes.Default): # all themes are based off Default
        submenu.exit() # exits current menu and goes to parent.
        global selectedTheme
        selectedTheme = submenu.selected
        menu.theme = theme
        menu.theme.init() # REQUIRED otherwise it will throw a tantrum lol
        menu.print(f"/zk/Successfully set theme to: /wk/{theme.theme_name}//")

    for theme in Themes.themelist: # themelist contains class references, not instances. - contains a list of all themes within the Themes class.
        thm = theme()
        submenu.AddOption(
            Option.Callable(
                f"{thm.theme_name}",
                f"{thm.theme_description} by {thm.theme_author}//",
                ChangeTheme,
                (thm,)
            )
        )

    submenu.selected = selectedTheme

    submenu.run()

def ScrollExample():
    submenu = Menu("Scroll Example", theme=menu.theme)

    for _ in range(50):
        submenu.AddOption(
            Option.Callable(
                f"Option {_+1}",
                "I do nothing.",
                None,
                ()
            )
        )

    submenu.run()

def ColourExample():
    """shows every colour in the foreground and background - not mixed, there'll be a LOT of options if they're mixed (256 options)"""
    submenu = Menu("/rx/C/yx/o/Gx/l/gx/o/cx/u/Bx/r/bx/s//!", theme=Themes.Colourless())

    codes = ["gx","Gx","bx","Bx","rx","Rx","yx","Yx","wx","mx","Mx","cx","Cx","kx","zx","xx"]

    submenu.AddOption(
            Option.Callable(
                f"/wx/Foreground /zx/Channels//",
                "Woah!",
                None,
                ()
            )
        )

    for code in codes:
        submenu.AddOption(
            Option.Callable(
                f"/{code}/{code}// (\\/{code}/)",
                "Woah!",
                menu.print,
                (f"/{code}/Colour Code:", code)
            )
        )

    submenu.AddOption(
            Option.Callable(
                f"/kw/Background/zk/ Channels//",
                "Woah!",
                None,
                ()
            )
        )

    for code in codes:
        submenu.AddOption(
            Option.Callable(
                f"/{code[::-1]}/{code[::-1]}// (\\/{code[::-1]}/)", # str[::-1] just reverses the string
                "Woah!",
                submenu.print,
                (f"/{code[::-1]}/Colour Code:", code[::-1])
            )
        )

    submenu() # you can also do this, instead of .run(), just something i should mention :P

menu.AddOption(
    Option.Callable(
        "Change Theme",
        "Themes? They exist?",
        ThemeChanger, # runs the themechanger submenu
        ()
    )
)

menu.AddOption(
    Option.Callable(
        "Open Scroll Example",
        "Opens a menu with about 50 options.\n- If you can't scroll, either zoom in or decrease terminal size.",
        ScrollExample,
        ()
    )
)

menu.AddOption(
    Option.Callable(
        "Open Colour Example",
        "Shows you all the possible colours! Ooh!",
        ColourExample,
        ()
    )
)

menu.AddOption(
    Option.Callable(
        "Say Hello!", # Name
        "Hey!",       # Description
        menu.print,   # Function
        ("Hey!",)     # Parameters (if there's only one, use a comma at the end, python will have an aneurysm if you dont)
    )
)

menu.AddOption(
    Option.Callable(
        "I'm disabled.",
        "Wow.",
        None,
        (),
        disabled=True # Optional disabled flag, defaults to False.
    )
)

menu.AddOption(
    Option.Boolean(
        "Boolean Option",
        "WHAT",
        True
    )
)

def PrintBoolOptionValue():
    """Prints the value of the boolean option."""
    boolean_option = menu.getOptionByIndex(-2)
    menu.print(f"Boolean Value: {boolean_option.value}")

menu.AddOption(
    Option.Callable(
        "Print boolean value",
        "Prints the value of the boolean option.",
        PrintBoolOptionValue,
        ()
    )
)

menu.run()