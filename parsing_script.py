"""World of Warships text mod.

Builds a global.mo where ship names (and other nation-specific strings) of
Japan, Russia and Pan-Asia come from the native-language translation, then
rewrites romanised Chinese/Japanese/Korean names into Chinese characters.

The game's default font for the EU/NA realm (Warhelios) has no CJK glyphs, so
the script also writes res_mods/gui/fontconfig_gameface.xml and
res_mods/gui/fontconfig_scaleform.xml, which point every realm at a font that
covers Latin, Cyrillic and CJK.
"""

import argparse
import os
import re

import polib

DEFAULT_WOWS_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\World of Warships"

# Languages whose global.mo gets replaced by the modded one.
TARGET_LANGUAGES = ("en", "ja")

# msgid pattern -> language the translation is taken from.
NATION_SOURCES = (
    (re.compile(r"^IDS_PJ[A-Z]{2}\d{3}|JAPAN"), "ja"),
    (re.compile(r"^IDS_PR[A-Z]{2}\d{3}|RUSSIA"), "ru"),
    (re.compile(r"^IDS_PZ[A-Z]{2}\d{3}|PAN_ASIA"), "zh_tw"),
)

# Applied in order, so full names must come before their parts.
NAME_REPLACEMENTS = (
    ("Tang Sanzang", "唐三藏"),
    ("Zhu Bajie", "豬八戒"),
    ("Sha Wujing", "沙悟淨"),
    ("Sun Wukong", "孫悟空"),
    ("Bajie", "八戒"),
    ("Wujing", "悟淨"),
    ("Wukong", "悟空"),
    ("Sanzang", "三藏"),

    ("Harbin", "哈爾濱"),
    ("Sejong", "世宗"),
    ("Huanghe", "黃河"),
    ("Dalian", "大連"),
    ("Fushun", "撫順"),
    ("Chung Mu", "忠武"),
    ("Anshan", "鞍山"),
    ("Sun Yat-Sen", "孫逸仙"),

    ("Yamato", "大和"),
    ("Kongō", "金剛"),
    ("Kirishima", "霧島"),
    ("Hiei", "比叡"),
    ("Haruna", "榛名"),
    ("Myōkō", "妙高"),
    ("Ashigara", "足柄"),
    ("Maya", "摩耶"),
    ("Nachi", "那智"),

    ("Xin Zhong Guo", "「新中國」"),
    ("Yamamoto Isoroku", "山本五十六"),
    ("Kunming", "昆明"),

    ("Mengchong", "蒙衝"),
    ("Incheon", "仁川"),
    ("Louchuan", "樓船"),
    ("Tianjin", "天津"),
    ("Taihang", "太行"),
    ("Lüshun", "旅順"),

    ("Taejong", "太宗"),
    ("Lanzhou", "蘭州"),

    ("Yimeng", "沂蒙"),
    ("Datong", "大同"),
    ("Baotou", "包頭"),
    ("Nanning", "南寧"),
)

REALMS = ("ASIA", "CN", "EU", "KO", "RU", "TH")

# CJK-capable fonts: (regular full name, regular path, bold full name, bold path).
FONTS = {
    # Ships with the game; the stock font for the ASIA realm.
    "source-han-sans": (
        "Source Han Sans JP Medium WH", "gui/fonts/Source_Han_Sans_JP_Medium_WH.ttf",
        "Source Han Sans JP Bold WH", "gui/fonts/Source_Han_Sans_JP_Bold_WH.ttf",
    ),
    # Aslain's "East Asia Font Pack": Warhelios look with CJK glyphs added.
    # Not part of the game, so it has to be installed in res_mods/gui/fonts.
    "warhelios-east-asia": (
        "Warhelios-east-asia-regular", "gui/fonts/Warhelios-east-asia-regular.ttf",
        "Warhelios-east-asia-bold", "gui/fonts/Warhelios-east-asia-bold.ttf",
    ),
}
BUNDLED_FONT = "source-han-sans"

# Same layout as the game's own gui/fontconfig_gameface.xml.
GAMEFACE_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>

<fontconfig>
    <fallback family="$WWSDefaultFont" />
    <fonts>
        <font family="$WWSDefaultFont" style="normal" weight="medium" >
{regular_srcs}
        </font>
        <font family="$WWSDefaultFontBold" style="normal" weight="bold" >
{bold_srcs}
        </font>
    </fonts>
</fontconfig>
"""

# One alias of the game's own gui/fontconfig_scaleform.xml.
SCALEFORM_ALIAS_TEMPLATE = """\
        <alias>
            <embedded> {embedded} </embedded>
            <fullName> {name} </fullName>
            <path> {path} </path>
            <bold> {bold} </bold>
            <italic> false </italic>
        </alias>"""


def parse_args():
    parser = argparse.ArgumentParser(description="World of Warships text mod.")
    parser.add_argument("--wows-dir", default=DEFAULT_WOWS_DIR,
                        help="World of Warships install folder (default: %(default)s)")
    parser.add_argument("--version",
                        help="game build folder under bin/ (default: the highest one); "
                             "set this when the launcher has preloaded the next build")
    parser.add_argument("--font", choices=sorted(FONTS),
                        help="font for every realm (default: warhelios-east-asia if it "
                             f"is installed in res_mods, otherwise {BUNDLED_FONT})")
    return parser.parse_args()


def load_catalog(build_dir, language):
    path = os.path.join(build_dir, "res", "texts", language, "LC_MESSAGES", "global.mo")
    return polib.mofile(path, encoding="utf-8")


def build_catalog(build_dir):
    en = load_catalog(build_dir, "en")
    sources = {language: load_catalog(build_dir, language)
               for language in {language for _, language in NATION_SOURCES}}

    output = polib.MOFile()
    output.metadata = en.metadata
    missing = 0
    for entry in en:
        for pattern, language in NATION_SOURCES:
            if pattern.search(entry.msgid):
                native = sources[language].find(entry.msgid)
                if native is None:
                    missing += 1
                else:
                    entry = native
                break
        output.append(entry)

    if missing:
        print(f"{missing} strings missing from the native catalogs, kept in English")
    return output


def replace_names(catalog):
    replacements = [(re.compile(re.escape(name), re.IGNORECASE), native)
                    for name, native in NAME_REPLACEMENTS]
    for entry in catalog:
        for pattern, native in replacements:
            entry.msgstr = pattern.sub(native, entry.msgstr)


def fontconfig_gameface(font):
    _, regular_path, _, bold_path = font

    def srcs(path):
        return "\n".join(f'            <src realm="{realm}" path="{path}" />'
                         for realm in REALMS)

    return GAMEFACE_TEMPLATE.format(regular_srcs=srcs(regular_path),
                                    bold_srcs=srcs(bold_path))


def fontconfig_scaleform(font):
    regular_name, regular_path, bold_name, bold_path = font
    aliases = "\n".join(
        SCALEFORM_ALIAS_TEMPLATE.format(embedded=embedded, name=name, path=path, bold=bold)
        for embedded, name, path, bold in (
            ("$WWSDefaultFont", regular_name, regular_path, "false"),
            ("$WWSDefaultFontBold", bold_name, bold_path, "true"),
            ("$IMELanguageBar", regular_name, regular_path, "false"),
            ("$IMECandidateListFont", regular_name, regular_path, "false"),
        )
    )
    realms = "\n".join(f"    <{realm}>\n{aliases}\n    </{realm}>" for realm in REALMS)
    return f'<?xml version="1.0" encoding="utf-8"?>\n\n<fontconfig>\n{realms}\n</fontconfig>\n'


def font_installed(res_mods_dir, font_key):
    _, regular_path, _, bold_path = FONTS[font_key]
    return all(os.path.exists(os.path.join(res_mods_dir, path))
               for path in (regular_path, bold_path))


def pick_font(res_mods_dir, requested):
    if requested:
        if requested != BUNDLED_FONT and not font_installed(res_mods_dir, requested):
            raise SystemExit(f"{requested} font files not found in {res_mods_dir}\\gui\\fonts")
        return requested
    if font_installed(res_mods_dir, "warhelios-east-asia"):
        return "warhelios-east-asia"
    return BUNDLED_FONT


def write_fontconfig(res_mods_dir, font_key):
    font = FONTS[font_key]
    gui_dir = os.path.join(res_mods_dir, "gui")
    os.makedirs(gui_dir, exist_ok=True)
    for name, content in (("fontconfig_gameface.xml", fontconfig_gameface(font)),
                          ("fontconfig_scaleform.xml", fontconfig_scaleform(font))):
        with open(os.path.join(gui_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)


def main():
    args = parse_args()
    bin_dir = os.path.join(args.wows_dir, "bin")
    version = args.version or max((d for d in os.listdir(bin_dir) if d.isdigit()), key=int)
    build_dir = os.path.join(bin_dir, version)
    res_mods_dir = os.path.join(build_dir, "res_mods")
    print(f"game build: {build_dir}")

    print("building global.mo")
    catalog = build_catalog(build_dir)
    replace_names(catalog)
    for language in TARGET_LANGUAGES:
        out_dir = os.path.join(res_mods_dir, "texts", language, "LC_MESSAGES")
        os.makedirs(out_dir, exist_ok=True)
        catalog.save(os.path.join(out_dir, "global.mo"))
        print(f"wrote {out_dir}\\global.mo")

    font_key = pick_font(res_mods_dir, args.font)
    write_fontconfig(res_mods_dir, font_key)
    print(f"wrote {res_mods_dir}\\gui\\fontconfig_*.xml using {font_key}")


if __name__ == "__main__":
    main()
