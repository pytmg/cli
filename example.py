from cli import CLI
import time

cli = CLI(title="Enhanced CLI Menu")

# 1. Add Main Menu Items
cli.addItem("Say \"Hello, User\"!")
cli.addItem("Open a Submenu")
cli.addItem("Show Current Time")
cli.addItem("/f red/Add a New Item/reset/")
cli.addItem("Does /e underline//e bold//e italic/NOTHING/reset/")

# 2. Functions for Menu Actions
def sayHello():
    cli.print("Hello, User!")

cli.addFunction(0, sayHello, ())

# 2a. Submenu Functionality
def openSubmenu():
    submenu = CLI(title="Submenu")
    submenu.addItem("Submenu Option 1")

    def submenuOption1():
        submenu.print("This is a submenu!")

    submenu.addFunction(0, submenuOption1, ())
    submenu.run(exitMessage="Go back")

cli.addFunction(1, openSubmenu, ())

# 2b. Show Current Time
def showTime():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    cli.print(f"The current time is: {current_time}")

cli.addFunction(2, showTime, ())

# 2c. Dynamic Item Addition
def addNewItem():
    print("Enter a name for the new item:")
    new_item = input("> ")
    cli.addItem(new_item)
    
    def newItemFunction():
        cli.print(f"You selected: {new_item}")

    cli.addFunction(len(cli.menu_items) - 2, newItemFunction, ())  # Bind function to the new item
    cli.print(f"New item added: {new_item}")

cli.addFunction(3, addNewItem, ())

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