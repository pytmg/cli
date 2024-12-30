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

CLI V2-beta is still in development. While it’s **way better** than before, full documentation isn’t ready yet.
The two big tasks left:
1. **Submenu support** – Now working like the old version!
2. **Colored options** – Still in progress. | May scrap though.

> [!WARNING]
> **Beta means bugs!**
> - **Known Crashes**:
>   - Resizing the terminal *too small* causes a crash (thanks, `curses`).
> - **Issues**:
>   - Sometimes the menu mysteriously disappears (*being worked on*).

---

### Additional Resources
- **Documentation**: [Documentation.md](./Documentation.md)
- **License**: [Ideal License (ILi)](./LICENSE)