# CLI-V1 Documentation

So, I've created my own CLI Menu script that is actually really easy to use.

## Table of Contents
- [CLI-V1 Documentation](#cli-v1-documentation)
  - [Table of Contents](#table-of-contents)
  - [What it is](#what-it-is)
  - [Installation](#installation)
    - [Modules](#modules)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Adding items](#adding-items)
    - [Running the script](#running-the-script)
      - [Creating a custom Exit function and name](#creating-a-custom-exit-function-and-name)
  - [Advanced Usage](#advanced-usage)
    - [Submenus](#submenus)

## What it is

It's essentially just a CLI Menu script, like `GRUB` if you know what that is, which works by pressing either the up or down arrow keys and enter.

## Installation

Download the `cli` GitHub Repository

- Using git
  - `git clone https://github.com/pytmg/cli.git`
- ZIP
  - [Download pytmg/cli ZIP](https://github.com/pytmg/cli/archive/refs/heads/main.zip)
  - and then extract it
  
> [!NOTE]
> Use `git clone` in the same directory as your project as it lets you update `cli` easier using `git pull`

Place the `cli` folder in the same directory as your script or in a specific folder you want to organize your dependencies.

```python
from Dependencies.cli import CLI
```

Use this if you have it under a directory called `Dependencies`, otherwise, use this

```python
from cli import CLI
```

`cli` is the main folder, and the `CLI` class is actually required for the script.

### Modules

Modules are handled by `cli/__init__.py`, if you don't have them, it will prompt you to install them.

> **Modules**
> - keyboard
> - ansi

That's it!

> [!NOTE]
> If you're on Windows 10, there's a good chance that ANSI won't render properly, so you need to run this command in your terminal: `REG ADD HKCU\Console /f /v VirtualTerminalLevel /t REG_DWORD /d 1`

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
@cli.item(name="Print \"Hello, World!\"")
def HelloWorld():
    cli.print("Hello, World!") # Use cli.print() rather than print() so that it shows up
```

> [!NOTE]
> You can still use `cli.addItem` if you have arguments, but if you don't, it's recommended to use `@cli.item`

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

cli.run(exitFunction=exitFunction, exitName="Exit Confirmation")
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

- If there's too much to put in one menu. simple as that.

Here's how

```python
from cli import CLI # Import CLI from cli/__init__.py if it's within the subdirectory "cli"

cli = CLI(title="Submenu Test")

@cli.item("Open submenu item")
def submenu1():
    # Create a new, independent CLI instance for the submenu.
    submenu = CLI(title="Submenu 1")

    @submenu.item("Hello!")
    def goodEvening(): # Function for the item
        submenu.print("Howdy!") # Prints "Howdy!"

    submenu.run(exitMessage="Go back") # Runs the submenu with a custom exit label

cli.run() # Run the main menu
```