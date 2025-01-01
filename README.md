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
> from cli.beta import CLI
> ```
> Check out the `example.py` file for changes and usage examples.

CLI V2-beta is still in development.
<small>*(But nearly done!!!)*</small>
 While it’s **way better** than before, full documentation isn’t ready yet.
The one big task left:
1. **Colored options** – Still in progress.
   - I may scrap this due to the fact that `curses` *is* kinda difficult to get some things working with, but, I'll try my best to get it working.

> [!WARNING]
> **Beta means bugs!**
> - **Known Crashes**:
>   - ~~Resizing the terminal *too small* causes a crash (thanks, `curses`).~~
>   - Now it tells you if the terminal is too small, and will continue when the terminal is big enough.
> - **Issues**:
>   - ~~Sometimes the menu mysteriously disappears~~ (*probably fixed*).
>   - I haven't been able to replicate this, probably after making a workaround for the resizing, but, IDK. Let me know if you manage to do it.

---

### Additional Resources
- **Documentation**
  - [V1 Documentation](./Documentation.md)
  - [V2-beta Documentation](./beta/Documentation.md)
- **License**: [Ideal License (ILi)](./LICENSE)