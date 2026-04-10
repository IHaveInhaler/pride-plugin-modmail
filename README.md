# Pride Plugin for Modmail

A [Modmail](https://github.com/modmail-dev/modmail) plugin that shows off pride flags with a `/pride` slash command (and `?pride` prefix command). Pick from 24 flags — the bot fetches the SVG from [pride-flag.dev](https://pride-flag.dev), renders it to a PNG, and posts it as an embed. 🏳️‍🌈

## Installation

### 1. System dependency

`cairosvg` (used to render the flag SVGs to PNG) depends on the system library **libcairo2**, which `pip` cannot install. Install it once on the host running your Modmail bot:

- **Debian / Ubuntu**: `sudo apt install libcairo2`
- **Arch**: `sudo pacman -S cairo`
- **Alpine**: `apk add cairo`
- **macOS**: `brew install cairo`
- **Windows**: see the [cairosvg docs](https://cairosvg.org/documentation/#installation)

If this library is missing, the plugin will fail to import with an error about `libcairo`.

### 2. Add the plugin to Modmail

In any channel where your Modmail bot listens, run:

```
?plugins add Lesbianbasedpriderainbowunicorn/pride-plugin-modmail/pride@main
```

Replace `Lesbianbasedpriderainbowunicorn/pride-plugin-modmail` with wherever this repo lives, and `main` with the branch you want to track. Modmail will:

1. Clone the repo.
2. Install anything listed in `pride/requirements.txt` (just `cairosvg`).
3. Load the plugin and register the command.

### 3. Sync the slash command (first install only)

Modmail registers `/pride` as a global application command. Discord can take up to an hour to propagate global commands the first time. If you want it available immediately, run once as the bot owner:

```
?eval await bot.tree.sync()
```

The `?pride` prefix command works right away regardless.

## Usage

- Slash: `/pride flag:<name>` — autocompletes from the 24 available flags.
- Prefix: `?pride <name>` — e.g. `?pride Lesbian`. Case-insensitive.

Running `?pride` with no argument lists every available flag.

## Permissions

The command requires Modmail's `REGULAR` permission level, which by default means anyone can use it. Adjust via Modmail's standard `?permissions` commands if you want to restrict it.
