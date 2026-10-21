# wows-text-mod
Text mod for World of Warships

This is a text mod for World of Warships that replaces all ship names with their native script:

Russian --> Cyrillic

Chinese, Japanese, Korean --> Chinese Characters


## Usage

```
pip install -r requirements.txt
python parsing_script.py
```

The script writes into the `res_mods` folder of the newest game build under `bin`:

- `texts/en/LC_MESSAGES/global.mo` and `texts/ja/LC_MESSAGES/global.mo` with the renamed ships
- `gui/fontconfig_gameface.xml` and `gui/fontconfig_scaleform.xml`, which switch every realm to a font with CJK glyphs (the stock EU/NA font, Warhelios, has none)

Options:

- `--wows-dir PATH` if the game is not installed in the default Steam folder
- `--version BUILD` to pick the build folder under `bin`, e.g. when the launcher has preloaded the next version
- `--font source-han-sans` uses Source Han Sans JP, which ships with the game
- `--font warhelios-east-asia` uses the Warhelios-style font from Aslain's "East Asia Font Pack"; it is picked automatically when it is already installed in `res_mods/gui/fonts`

Run the script again after every game update, and after reapplying a modpack that rewrites `res_mods`.

## Font config

The game no longer reads `res_mods/fontconfig.xml`. Fonts are now configured per realm in two files under `gui/`: `fontconfig_scaleform.xml` (Scaleform UI, same layout as the old file) and `fontconfig_gameface.xml` (Gameface UI). The script overrides both.

## Requirements
polib
