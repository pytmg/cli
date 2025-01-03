# CLI Script

![Total Commits](https://badgen.net/github/commits/pytmg/cli?color=black&icon=github)

Made for folks who want to create a CLI script but can’t be bothered with the hassle.

It’s **super easy to use**:
1. Download the `cli` folder.
2. Add this to your script:
   ```python
   from cli import CLI
   ```
3. Check out the Docs - [Documentation.md](./Documentation.md)
4. Have fun building! 🎉

---

## About CLI V2-beta

> **Usage**:
> ```python
> from cli.beta import CLI, Option
> ```
> Check out the `example.py` file for changes and usage examples.

CLI V2-beta is still in development.
<small>*(But nearly done!!!)*</small>

While it’s **way better** than before, there are still some bugs I need to polish out.

1. **Colored options** – not gonna do it.
   - ~~Might give up, given `curses` is a pain in the arse but I'll try to get it working.~~ i can't be asked lol

> [!WARNING]
> **Beta means bugs!**
> - **Known Crashes**:
>   - ~~Resizing the terminal *too small* causes a crash (thanks, `curses`).~~
>   - Now it tells you if the terminal is too small, and will continue when the terminal is big enough... *maybe* (depends on how `curses` is feeling like treating you).
> - **Issues**:
>   - ~~Sometimes the menu mysteriously disappears~~ (*probably fixed??*).
>   - Haven’t been able to replicate it lately, but let me know if you can. It might’ve been patched after the resizing workaround.

---

## UNIX Usage

There are *some* issues with Linux and this CLI menu shenanagin, BUT, you can [fork](https://github.com/pytmg/cli/fork) this repository, and make a fix for UNIX Systems!

---

### Additional Resources
- **Documentation**
  - [V1 Documentation](./Documentation.md)
  - [V2-beta Documentation](./beta/Documentation.md)
- **License**: [Ideal License (ILi)](./LICENSE)