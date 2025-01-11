try:
    import keyboard
    import ansi
    import os
except ModuleNotFoundError:
    try:
        import os
    except ModuleNotFoundError:
        input("How do you not even have OS?\nAnyway, open a terminal window and type \"pip install ansi keyboard\" for the required modules.\n\nPress Enter to dismiss.")
        exit()
    if input("Install \"ansi\" and \"keyboard\"? (Y/n)\n> ").lower().startswith("y"):
        os.system("pip install keyboard ansi")
    else:
        input("Alright then.\n\nPress Enter to dismiss.")
        exit()
        
printStatement = ""
def print(*args, **kwargs):
    global printStatement
    __builtins__.print(*args, **kwargs)
    printStatement = " ".join(args)
MenuItems = [
    "Say \"Hello, World!\"",
    "Credits",
] + ["Exit"] # Exit is required.
Colours = {
    "/f red/": f"{ansi.color.fg.red}",
    "/b red/": f"{ansi.color.bg.red}",
    "/f green/": f"{ansi.color.fg.green}",
    "/b green/": f"{ansi.color.bg.green}"
}
Title = "Test"
SelectedIndex = 0
class Console():
    @staticmethod
    def cls():
        os.system("cls" if os.name == "nt" else "clear")
def Refresh() -> None:
    Console.cls()
    __builtins__.print(Title)
    for i, item in enumerate(MenuItems):
        formattedItem = item
        for color in Colours:
            formattedItem = formattedItem.replace(color, Colours[color]).replace("/reset/", f"{ansi.color.bg.white}{ansi.color.fg.black}" if i == SelectedIndex else f"{ansi.color.fx.reset}")
        __builtins__.print("\n".join([f"{f"{ansi.color.bg.white}{ansi.color.fg.black}>" if i == SelectedIndex else " "} {formattedItem}"]) + f"{ansi.color.fx.reset}")
    __builtins__.print("Use UP and DOWN arrow to navigate, press ENTER to select." )
    __builtins__.print(printStatement)
    
Refresh()
while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "down":
            SelectedIndex += 1
            SelectedIndex %= len(MenuItems)
            Refresh()
        if event.name == "up":
            SelectedIndex -= 1
            SelectedIndex %= len(MenuItems)
            Refresh()
        if event.name == "enter":
            # Add functions here
            if SelectedIndex == 0:
                print("Hello, World!")
                Refresh() # Always add `Refresh()` AFTER any print statements.
                continue # Always add `continue` otherwise it'll refresh without printing anything.
            if SelectedIndex == 1:
                print("Creator: TMG")
                Refresh()
                continue
            # Required
            if SelectedIndex == len(MenuItems)-1:
                break
            Refresh()