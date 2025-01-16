# CLI-V2 Documentation

Ever wanted CLI Menus to be easier to create? Worry no more with CLI-V2!

## Table of Contents
- [CLI-V2 Documentation](#cli-v2-documentation)
  - [Table of Contents](#table-of-contents)
  - [What it is](#what-it-is)
  - [Installation](#installation)
    - [Modules](#modules)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Adding items](#adding-items)
      - [Option Types](#option-types)
        - [Option.Default](#optiondefault)
        - [Option.Boolean](#optionboolean)
        - [Option.Input](#optioninput)
          - [Number](#number)
          - [String](#string)
    - [Running the script](#running-the-script)
      - [Creating a custom Exit function and name](#creating-a-custom-exit-function-and-name)
    - [Customisability](#customisability)
      - [Config](#config)
      - [Border](#border)

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
from Dependencies.cli import CLI, Option
```

Use this if you have it under a directory called `Dependencies`, otherwise, use this

```python
from cli import CLI, Option
```

`cli` is the main folder, and the `CLI` and `Option` classes are actually required for the script.

### Modules

There are no modules required, but, you can also install `windows-curses` if you're on Windows and don't have `curses`.

> - windows-curses
>   - for.. compatibility.

That's it!

> [!NOTE]
> If you're on Windows 10, there's a decent chance that ANSI won't render properly, so you need to run this command in your terminal: `REG ADD HKCU\Console /f /v VirtualTerminalLevel /t REG_DWORD /d 1`

## Usage

### Initialization

Once you have `cli` installed and the class `CLI` imported, you can do

```python
cli = CLI(title="My amazing CLI Script")
```

This initializes a CLI object with the title `My amazing CLI Script`, this will appear when you start the CLI.

### Adding items

There are different types of items for CLI.

- Default
  - The default CLI Option, you need to define and use a function for this one.
- Boolean
  - Just an on-off switch
- Input
  - Number
    - Integer input - You can use the numpad OR number row on your keyboard.
  - String
    - String input - Just that.

#### Option Types

##### Option.Default

All you need is a function, really.

```python
NewOption = Option.Default(
    name="Custom Option",
    description="Shows the time!",
    cli.print, # Default print function in CLI()
    (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) # import time btw
)

cli.addItem(NewOption)
```

Example output: `2024-12-31 14:30:45`

##### Option.Boolean

Really simple!

```python
NewBoolOption = Option.Boolean(
    name="Boolean!",
    description="On/Off",
    default=False
)

NewBoolOptionIDX = cli.addItem(NewBoolOption)

cli.getValueByIndex(NewBoolOptionIDX) # Returns the value of NewBoolOption when called
```

You can also call `getValueByName` instead if you want to get it by name.

Example:

False
```
Boolean! [ ]
```
or True
```
Boolean! [x]
```

##### Option.Input

Both of these open an input window.

###### Number

```python
NewNumberOption = Option.Input.Number(
    name="Number",
    description="Input a number!",
    default=0
)

cli.addItem(NewNumberOption)
```

You can read the value with either `cli.getValueByName` or `cli.getValueByIndex`.

`cli.addItem` does also return the index of the item when added!

###### String

```python
NewStringOption = Option.Input.String(
    name="String",
    description="Input a string!",
    default=""
)

cli.addItem(NewStringOption)
```

Same as [Number](#number), you can read the value with `cli.getValueByName` or `cli.getValueByIndex`.

### Running the script

To be able to run the script, you must run the `cli` class.

```python
cli.run()
```

---

#### Creating a custom Exit function and name

To create a custom function for the Exit, rather than outright exiting the current menu, you can just do something like this:

```python
def exitFunction():
  if input("Are you sure? (Y/n)\n> ").lower().startswith("y"):
    cli.exit()

cli.run(exitFunction=exitFunction, exitLabel="Exit Confirmation")
```

> [!TIP]
> Add `cli.exit()` to your exit function to make it easier for the user to exit the menu. Without it, the user might get stuck in the menu or submenu.

---

This runs the cli object with all the functions and items you have created.

### Customisability

You can add more customisability with the `Config` and `Border` classes.

#### Config

This lets you toggle on or off, to your liking, the following:
- Output Area
- Description Area
- Title
- AutoResizing (Recommended to keep ON)

Example Usage

```python
from cli import CLI, Option, Config

cfg = Config(ShowTitle=False) # Disables the title at the top

cli = CLI(title="None", config=cfg)

# You can also run `cli.config = cfg` if you don't add it on initialisation

cli.run() # Just adds the Exit option :)
```

And you'll notice it doesn't say `None` anywhere.

Output and Descriptions can be toggled off, this also removes the boxes, so if you have a lot of options and don't care about the descriptions nor outputs, you can turn these off.

#### Border

Borders are defined within the `Border` class in `__init__.py`, you can add more if you want, by going into the code.
- Lines `114` to `124` in `__init__.py` are the lines you'll have to add to.
- Along with `109` just to add the name.

Example Usage

```python
# Assuming there's still only Double and Single

from cli import CLI, Option, Border

border = Border(Type="Single")

cli = CLI(borders=border)

# And again, you can also run `cli.border = border` if you don't add it on initialisation.

cli.run()
```
