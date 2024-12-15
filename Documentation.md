# CLI Documentation

So, I've created my own CLI Menu script that is actually really easy to use.

## Installation

Get the `cli.py` file from [here](https://raw.githubusercontent.com/pytmg/cli/refs/heads/main/cli.py)

Place it in the same directory as your script or in a specific folder you want to organize your dependencies.

```python
from Dependencies.cli import CLI
```

Use this if you have it under a directory called `Dependencies`, otherwise, use this

```python
from cli import CLI
```

`cli` is the main file, and the `CLI` class is actually required for the script.

### Modules

Modules are handled by `cli.py`, if you don't have them, it will prompt you to install them.

That's it!

## Usage

### Initialization

Once you have `cli` installed and the class `CLI` imported, you can do

```python
cli = CLI(title="My amazing CLI Script")
```

This initializes a CLI object with the title `My amazing CLI Script`, this will appear when you start the CLI.

### Adding items

To add a menu item, you're going to need a name and a function.

```python
cli.addItem("Print \"Hello, World!\"")

def HelloWorld():
    cli.print("Hello, World!") # Use cli.print() rather than print() so that it shows up

cli.addFunction(0, HelloWorld, ()) # idx, function, parameters
```

What this does is create an item called `Print "Hello, World!"` and it has a function called `HelloWorld` without parameters, and all it does is print `Hello, World!` when executed. Then it adds the function to that item by index, so if `Print "Hello, World!"` is the first thing you added, the index will be 0.

### Running the script

To be able to run the script, you must run the `cli` object.

```python
cli.run()
```

This runs the cli object with all the functions and items you have created

You should be greeted with this once you run the script with Python.

```
My amazing CLI Script
> Print "Hello, World!"
  Exit
Use UP and DOWN arrow to navigate, press ENTER to select.
```

When pressing ENTER while the first option is selected, it should look like this afterward.

```
My amazing CLI Script
> Print "Hello, World!"
  Exit
Use UP and DOWN arrow to navigate, press ENTER to select.
Hello, World!
```

You can also navigate to `Exit` and it'll exit gracefully.

## Advanced Usage

### Submenus

I know, I know, you really want to know how to use submenus and that is FULLY understandable..

Why would you need sub-menus?

- If there's too much to put in one menu

Here's how

```python
cli = CLI(title="Submenu Test")

cli.addItem("Open submenu item")

def submenu1():
    submenu = CLI(title="Submenu 1") # Initialize the submenu

    submenu.addItem("Hello!") # Add an item

    def goodEvening(): # Function for the item
        submenu.print("Good evening") # Prints "Good evening"

    submenu.addFunction(0, goodEvening, ()) # Adds the function to the item

    submenu.run() # Runs the submenu

cli.addFunction(0, submenu1, ()) # Or whatever index it is

cli.run() # Run the main menu
```