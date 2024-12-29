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