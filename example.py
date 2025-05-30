# Example script for CLI-V3beta1

from __init__ import Menu, Option, Themes # use cli instead of __init__

menu = Menu("Wow!")

def ThemeChanger():
    submenu = Menu("Theme Changer", theme=menu.theme)

    def ChangeTheme(theme: Themes.Default): # all themes are based off Default
        submenu.exit()
        menu.theme = theme
        menu.theme.init()

    for theme in Themes.themelist:
        thm = theme()
        submenu.AddOption(
            Option(
                f"{thm.theme_name}",
                f"{thm.theme_description} by {thm.theme_author}//",
                ChangeTheme,
                (thm,)
            )
        )

    submenu.run()

menu.AddOption(
    Option(
        "Change Theme",
        "Themes? They exist?",
        ThemeChanger,
        ()
    )
)

menu.AddOption(
    Option(
        "Say Hello!",
        "Hey!",
        menu.print,
        ("Hey!",)
    )
)

menu.AddOption(
    Option(
        "I'm disabled.",
        "Wow.",
        None,
        (),
        disabled=True
    )
)

menu.run()