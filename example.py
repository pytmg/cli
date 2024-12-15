from cli import CLI
import time

cli = CLI(title="Enhanced CLI Menu")

# 1. Add Main Menu Items
cli.addItem("Say \"Hello, User\"!")
cli.addItem("Open a Submenu")
cli.addItem("Show Current Time")
cli.addItem("/f red/Add a New Item/reset/")
cli.addItem("/f yellow/Exit Program/reset/")

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
    submenu.run()

cli.addFunction(1, openSubmenu, ())

# 2b. Show Current Time
def showTime():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    cli.print(f"The current time is: {current_time}")

cli.addFunction(2, showTime, ())

# 2c. Dynamic Item Addition
def addNewItem():
    cli.print("Enter a name for the new item:")
    new_item = input("> ")
    cli.addItem(new_item)
    
    def newItemFunction():
        cli.print(f"You selected: {new_item}")

    cli.addFunction(len(cli.menu_items) - 2, newItemFunction, ())  # Bind function to the new item

cli.addFunction(3, addNewItem, ())

# 2d. Exit Confirmation
def confirmExit():
    cli.print("Are you sure you want to exit? (Y/n)")
    response = input("> ")
    if response.lower().startswith("y"):
        cli.print("Goodbye!")
        time.sleep(1)
        cli.cls()
        exit()
    else:
        cli.print("Returning to the menu...")

cli.addFunction(4, confirmExit, ())

# 3. Run the Menu
cli.run()
