# CLI Script

![Total Commits](https://badgen.net/github/commits/pytmg/cli?color=black&icon=github)

Created for those who want to make a CLI script, but cannot be asked with it.

Really easy to use, you just download the `cli` folder, use `from cli import CLI` and have fun with it!

---

To be expected:
Expect a new version where it uses `curses` rather than `keyboard` + `ansi` modules, for easier use and less obstruction.
- Obstructions at the moment
  - Needing to install `keyboard` and `ansi`
  - `keyboard` requires root access on UNIX systems
  - `keyboard` takes control of the keyboard entirely across the whole system, stopping other apps from taking input
- Fixes when using `curses`
  - `curses` is built into Python
  - `curses` won't\* require root access
  - `curses` won't\* take control of the keyboard throughout the whole system

> [!NOTE]
> I haven't tested `curses` on UNIX systems yet, I will do that before releasing the new version.

> [!NOTE]
> I haven't tested keyboard input yet on `curses` - Will do soon

---

Documentation: [Documentation.md](./Documentation.md)

LICENSE: [Ideal License (ILi)](./LICENSE)
