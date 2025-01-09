from __init__ import ( CLI, Option ) # cli.beta

cli = CLI(title="pytmg CLI | V2-beta")

cli.addItem(Option.Default(
    name="Option 1",
    description="Prints \"Hello, World!\"",
    function=cli.print,
    args=("Hello, World!")
))
def createOption():
    NAME = cli.input("Name")
    if NAME:
        DESCRIPTION = cli.input("Description")
        if DESCRIPTION:
            OUTPUT = cli.input("Output")
            if OUTPUT:
                KEYBIND = cli.input("Keybind - Press ESC to not have one")
                cli.addItem(Option.Default(
                    name=NAME,
                    description=DESCRIPTION + "\n\nCreated with Option Creator",
                    function=cli.print,
                    args=(OUTPUT),
                    keybind=KEYBIND
                ))
                cli.print("Created new Option")
            else:
                cli.print("Cancelled creation.")
        else:
            cli.print("Cancelled creation.")
    else:
        cli.print("Cancelled creation.")

cli.addItem(Option.Default(
    name="Option Creator",
    description="Create any named option lol",
    function=createOption,
    args=(),
    keybind="c"
))
def openSubmenu():
    submenu = CLI(title="Submenu")

    submenu.addItem(Option.Default("Submenu Option 1", "Submenu Option 1", submenu.print, ("Yuh.",)))
    
    submenu.run(exitLabel="Go back", exitDescription="Go back to the main menu") # Make the "Exit" message show as Go Back

cli.addItem(Option.Default(
    name="Submenu Test 1",
    description="Opens a submenu",
    function=openSubmenu,
    args=(),
    keybind="s"
))

cli.addItem(Option.Default(
    name="Really long description",
    description="This is a really long description inherently designed to test the fucking script because I am completely unsure if this works fully or not, because I am delusional.",
    function=cli.print,
    args=("This is a really long output inherently designed to test the fucking script because I am completely unsure if this works fully or not, because I am delusional.")
))

cli.addItem(Option.Boolean(
    name="Woah!",
    description="This is a boolean option",
    default=False,
    keybind="b"
))

cli.run()