# CLI-V2-beta Documentation

CLI-V2-beta is a version of CLI that is not fully completed yet, but here is the current Documentation for it as of 3/Jan/25, and yes, that means it's very likely to change in future.

## Table of Contents
- [CLI-V2-beta Documentation](#cli-v2-beta-documentation)
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
from Dependencies.cli.beta import CLI
```

Use this if you have it under a directory called `Dependencies`, otherwise, use this

```python
from cli.beta import CLI, Option
```

`cli` is the main folder, and the `CLI` and `Option` classes are actually required for the script.

### Modules

There are no modules *required*, but at the moment, but for some ungodly reason, importing `cli.beta` inflicts the MAIN `cli` file, which kinda forces you to install the required modules for V1. It's stupid, but you can install them and get it over with.

> [!NOTE]
> Once V2 is fully done, V1 will be put in a seperate folder, so that it doesn't force unnecessary module installation.

> **Modules**
> - keyboard
> - ansi

and if you're on Windows

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