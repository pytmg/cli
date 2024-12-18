from cli import CLI
import time

cli = CLI(title="Enhanced CLI Menu")

# 1. Function Creation
def sayHello():
    cli.print("Hello, User")

# 1a. Submenu Functionality
def openSubmenu():
    submenu = CLI(title="Submenu")

    def submenuOption1():
        submenu.print(f"This is a submenu!")

    submenu.addItem("Submenu Option 1", submenuOption1, ())
    submenu.run(exitMessage="Go back") # Make the "Exit" message show as Go Back

# 1b. Show Current Time
def showTime():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    cli.print(f"The current time is: {current_time}")

# 1c. Dynamic Item Addition
def addNewItem():
    print("Enter a name for the new item:")
    new_item = input("> ")
    
    def newItemFunction():
        cli.print(f"You selected: {new_item}")

    cli.addItem(new_item, newItemFunction, ())
    cli.print(f"New item added: {new_item}")

# 1. Add Main Menu Items
cli.addItem("Say \"Hello, User\"!", sayHello, ())
cli.addItem("Open a Submenu", openSubmenu, ())
cli.addItem("Show Current Time", showTime, ())
cli.addItem("/f red/Add a New Item/reset/", addNewItem, ())
cli.addItem("Does /e underline//e bold//e italic/NOTHING/reset/", cli.doNothing, ())

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