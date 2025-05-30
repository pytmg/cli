# Example script for CLI-V3beta1

from cli import Menu, Option, Themes

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

    for theme in Themes.themelist: # themelist contains class references, not instances.
        thm = theme()
        submenu.AddOption(
            Option(
                f"{thm.theme_name}",
                f"{thm.theme_description} by {thm.theme_author}//",
                ChangeTheme,
                (thm,)
            )
        )

    submenu.selected = selectedTheme

    submenu.run()

menu.AddOption(
    Option(
        "Change Theme",
        "Themes? They exist?",
        ThemeChanger, # runs the themechanger submenu
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