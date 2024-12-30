UseBeta = False

if not UseBeta:
    from __init__ import ( CLI ) # THIS ONLY APPLIES FOR THE EXAMPLE
    # USE `from cli import CLI` IF YOU HAVE IT IN A SEPARATE FOLDER
    import time

    cli = CLI(title="Enhanced CLI Menu")

    # 1. Function creation
    @cli.item(name="Say \"Hello, User\"!")
    def sayHello():
        cli.print("Hello, User")

    # 1a. Submenu Functionality
    @cli.item("Open a Submenu")
    def openSubmenu():
        submenu = CLI(title="Submenu")

        @submenu.item(name="Submenu Option 1")
        def submenuOption1():
            submenu.print(f"This is a submenu!")
        
        submenu.run(exitMessage="Go back") # Make the "Exit" message show as Go Back

    # 1b. Show Current Time
    @cli.item(name="Show current time")
    def showTime():
        current_time = time.strftime("%H:%M:%S", time.localtime())
        cli.print(f"The current time is: {current_time}")

    # 1c. Dynamic Item Addition
    @cli.item(name="/f red/Add a new item/reset/")
    def addNewItem():
        print("Enter a name for the new item:")
        new_item = input("> ") # Wait for input
        
        def newItemFunction(): # Create a function for the new item
            cli.print(f"You selected: {new_item}")

        cli.addItem(new_item, newItemFunction, ())
        cli.print(f"New item added: {new_item}") # Notice

    cli.addItem("Does /e underline//e bold//e italic/NOTHING/reset/", cli.doNothing, ()) # NOTHING!!!

    # 2d. Exit Confirmation
    def confirmExit(): # No parameters as it will not matter
        print("Are you sure you want to exit? (Y/n)")
        response = input("> ")
        if response.lower().startswith("y"):
            print("Goodbye!")
            time.sleep(1)
            cli.exit()
        else:
            cli.refresh()

    # 3. Run the Menu with a custom "Exit" option
    cli.run(exitMessage="/f yellow/Exit/reset/", exitFunction=confirmExit)
else:
    """
    THIS IS A BETA VERSION OF CLI
    
    THIS IS NOT DONE SO IT HAS SOME FEATURES NOT ADDED YET - such as coloured options and submenus
    """
    
    from beta import ( CLI )

    cli = CLI(title="pytmg CLI | V2-beta")

    cli.addItem(
        name="Option 1",
        description="Prints \"Hello, World!\"",
        function=cli.print,
        args=("Hello, World!")

    )
    def createOption():
        NAME = cli.input("Name")
        if NAME:
            DESCRIPTION = cli.input("Description")
            if DESCRIPTION:
                OUTPUT = cli.input("Output")
                if OUTPUT:
                    KEYBIND = cli.input("Keybind - Press ESC to not have one")
                    cli.addItem(
                        name=NAME,
                        description=DESCRIPTION + "\n\nCreated with Option Creator",
                        function=cli.print,
                        args=(OUTPUT),
                        keybind=KEYBIND
                    )
                    cli.print("Created new Option")
                else:
                    cli.print("Cancelled creation.")
            else:
                cli.print("Cancelled creation.")
        else:
            cli.print("Cancelled creation.")

    cli.addItem(
        name="Option Creator",
        description="Create any named option lol",
        function=createOption,
        args=(),
        keybind="c"
    )
    def openSubmenu():
        submenu = CLI(title="Submenu")

        submenu.addItem("Submenu Option 1", "Submenu Option 1", submenu.print, ("Yuh."))
        
        submenu.run(exitLabel="Go back", exitDescription="Go back to the main menu") # Make the "Exit" message show as Go Back

    cli.addItem(
        name="Submenu Test 1",
        description="Opens a submenu",
        function=openSubmenu,
        args=(),
        keybind="s"
    )

    cli.addItem(
        name="Really long description",
        description="This is a really long description inherently designed to test the fucking script because I am completely unsure if this works fully or not, because I am delusional.",
        function=cli.print,
        args=("This is a really long output inherently designed to test the fucking script because I am completely unsure if this works fully or not, because I am delusional.")
    )

    cli.run()