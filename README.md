# wows-text-mod
Text mod for World of Warships

This is a text mod for World of Warships that shows ship names in their native script:

- Russian ships: Cyrillic, from the game's Russian translation
- Japanese ships: Japanese, from the game's Japanese translation
- Pan-Asian ships: Traditional Chinese, from the game's Traditional Chinese translation
- Chinese, Japanese and Korean names that are still romanised after that (Pan-Asian ships, Arpeggio and campaign names and so on): Chinese characters, from a hand-written table

It works with the client language set to English. Everything else in the client stays in English.

## Usage

```
pip install -r requirements.txt
python parsing_script.py
```

The script writes into the `res_mods` folder of the newest game build under `bin`:

- `texts/en/LC_MESSAGES/global.mo` with the renamed ships
- `gui/fonts/textmod-regular.ttf` and `gui/fonts/textmod-bold.ttf`: a CJK font with every glyph it lacks copied in from the stock Warhelios font (Polish letters, the ★ supership icon, the game's private-use icons)
- `gui/fontconfig_gameface.xml` and `gui/fontconfig_scaleform.xml`, which switch every realm to that font (the stock EU/NA font, Warhelios, has no CJK glyphs)

Run the script again after every game update, and after reapplying a modpack that rewrites `res_mods`.

Options:

- `--wows-dir PATH` if the game is not installed in the default Steam folder
- `--version BUILD` to pick the build folder under `bin`, e.g. when the launcher has preloaded the next version
- `--font source-han-sans` (the default) builds on Source Han Sans JP, which ships with the game, so nothing else needs to be installed
- `--font warhelios-east-asia` builds on the Warhelios-style font from Aslain's "East Asia Font Pack" instead. This is optional; it is picked automatically when the pack is already installed in `res_mods/gui/fonts`

## How it works

The romanised-to-Chinese-character names live in `NAME_REPLACEMENTS` in `parsing_script.py`. The game's own translations can't supply them, since no client language has these names in characters, so the table is maintained by hand. Names are matched as whole words, case-insensitively, so e.g. "Harbinger" or "Mayan" are left alone. Entries are applied in order, so a full name has to come before its parts.

The game no longer reads `res_mods/fontconfig.xml`. Fonts are configured per realm in `gui/fontconfig_scaleform.xml` (Scaleform UI) and `gui/fontconfig_gameface.xml` (Gameface UI), and the script overrides both. The stock fonts are read straight from the game's `res_packages`.

## Requirements
Python 3.9+, polib, fonttools
