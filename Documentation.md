# CLI Documentation

So, I've created my own CLI Menu script that is actually really easy to use.

## What it is

It's essentially just a CLI Menu script, like `GRUB` if you know what that is, which works by pressing either the up or down arrow keys and enter.

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
def HelloWorld():
    cli.print("Hello, World!") # Use cli.print() rather than print() so that it shows up

cli.addItem("Print \"Hello, World!\"", HelloWorld, ()) # name, function, parameters
```

> [!IMPORTANT]
> Item creation was changed in the most recent update, so update your scripts if necessary.
> <br>**What changed**:
> - `addItem` and `addFunction` were merged, so rather than running `cli.addItem(name)` then `cli.addFunction(index, function, params)`, you can run `cli.addItem(name, function, params)`

What this does is define a new function called `HelloWorld` that prints `"Hello, World!"` when run in the CLI, then creates a new item with the name `Print "Hello, World!"` with that function and no parameters.

### Running the script

To be able to run the script, you must run the `cli` object.

```python
cli.run()
```

---

#### Creating a custom Exit function and name

To create a custom function for the Exit, rather than outright exiting the current menu, you can just do something like this:

```python
def exitFunction(): # No parameters!!
  if input("Are you sure? (Y/n)\n> ").lower().startswith("y"):
    cli.exit()

cli.run(exitFunction=exitFunction)
```

> [!TIP]
> Add `cli.exit()` to your exit function to make it easier for the user to exit the menu. Without it, the user might get stuck in the menu or submenu.

---

This runs the cli object with all the functions and items you have created.

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

> [!NOTE]
> There is a bit of a flicker when printing something, but it isn't exactly noticable.

You can also navigate to `Exit` and it'll exit gracefully.

## Advanced Usage

### Submenus

I know, I know, you really want to know how to use submenus and that is FULLY understandable..

Why would you need sub-menus?

- If there's too much to put in one menu

Here's how

```python
from cli import CLI # Import CLI from cli.py if it's within the same directory

cli = CLI(title="Submenu Test")

def submenu1():
    submenu = CLI(title="Submenu 1") # Initialize the submenu

    def goodEvening(): # Function for the item
        submenu.print("Good evening") # Prints "Good evening"

    submenu.addItem("Hello!", goodEvening, ()) # Add an item with the goodEvening function

    submenu.run() # Runs the submenu

cli.addItem("Open submenu item", submenu1, ())

cli.run() # Run the main menu
```