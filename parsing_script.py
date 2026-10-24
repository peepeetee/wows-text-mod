"""World of Warships text mod.

Builds a global.mo where ship names (and other nation-specific strings) of
Japan, Russia and Pan-Asia come from the native-language translation, then
rewrites romanised Chinese/Japanese/Korean names into Chinese characters.

The game's default font for the EU/NA realm (Warhelios) has no CJK glyphs, so
the script also builds a CJK font with every glyph of the stock Warhelios
(Polish letters, the supership star, the game's private-use icons) copied in,
and writes res_mods/gui/fontconfig_gameface.xml and
res_mods/gui/fontconfig_scaleform.xml to use it for every realm.
"""

import argparse
import functools
import io
import os
import re
import struct
import zlib

import polib
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

DEFAULT_WOWS_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\World of Warships"

# Languages whose global.mo gets replaced by the modded one.
TARGET_LANGUAGES = ("en",)

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

# CJK fonts the patched font is built on: (regular path, bold path).
FONTS = {
    # Ships with the game; the stock font for the ASIA realm.
    "source-han-sans": (
        "gui/fonts/Source_Han_Sans_JP_Medium_WH.ttf",
        "gui/fonts/Source_Han_Sans_JP_Bold_WH.ttf",
    ),
    # Aslain's "East Asia Font Pack": Warhelios look with CJK glyphs added.
    # Not part of the game, so it has to be installed in res_mods/gui/fonts.
    "warhelios-east-asia": (
        "gui/fonts/Warhelios-east-asia-regular.ttf",
        "gui/fonts/Warhelios-east-asia-bold.ttf",
    ),
}
BUNDLED_FONT = "source-han-sans"

# Stock EU font; any glyph the CJK font lacks is copied from here.
STOCK_FONTS = ("gui/fonts/Warhelios_Regular.ttf", "gui/fonts/Warhelios_Bold.ttf")
PATCHED_FONTS = ("gui/fonts/textmod-regular.ttf", "gui/fonts/textmod-bold.ttf")

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
    # Whole words only, so e.g. "harbinger" and "Mayan" are left alone.
    replacements = [(re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE), native)
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


@functools.cache
def load_package_index(wows_dir, build_dir, package):
    """Map file paths to (package file, offset, size, unpacked size) from bin/<build>/idx."""
    with open(os.path.join(build_dir, "idx", package + ".idx"), "rb") as f:
        idx = f.read()
    nodes_count, files_count = struct.unpack_from("<II", idx, 16)
    nodes_offset, files_offset, volumes_offset = (
        offset + 16 for offset in struct.unpack_from("<QQQ", idx, 32))

    def string_at(record, length, pointer):
        return idx[record + pointer:record + pointer + length].rstrip(b"\0").decode()

    # Nodes form a tree of path components: (name length, name pointer, id, parent id).
    nodes = {}
    for i in range(nodes_count):
        record = nodes_offset + 32 * i
        name_length, name_pointer, node_id, parent_id = struct.unpack_from("<QQQQ", idx, record)
        nodes[node_id] = (string_at(record, name_length, name_pointer), parent_id)

    def node_path(node_id):
        parts = []
        while node_id in nodes:
            name, node_id = nodes[node_id]
            parts.append(name)
        return "/".join(reversed(parts))

    name_length, name_pointer = struct.unpack_from("<QQ", idx, volumes_offset)
    volume_path = os.path.join(wows_dir, "res_packages",
                               string_at(volumes_offset, name_length, name_pointer))

    files = {}
    for i in range(files_count):
        node_id, _, offset, _, size, _, unpacked_size, _ = struct.unpack_from(
            "<QQQQIIII", idx, files_offset + 48 * i)
        files[node_path(node_id)] = (volume_path, offset, size, unpacked_size)
    return files


def read_packaged_file(wows_dir, build_dir, path, package="gui"):
    """Read a file from the game's res_packages."""
    files = load_package_index(wows_dir, build_dir, package)
    if path not in files:
        raise SystemExit(f"{path} not found in {package}.idx")
    volume_path, offset, size, unpacked_size = files[path]
    with open(volume_path, "rb") as f:
        f.seek(offset)
        data = f.read(size)
    return data if size == unpacked_size else zlib.decompress(data, -zlib.MAX_WBITS)


def font_installed(res_mods_dir, font_key):
    return all(os.path.exists(os.path.join(res_mods_dir, path)) for path in FONTS[font_key])


def pick_font(res_mods_dir, requested):
    if requested:
        if requested != BUNDLED_FONT and not font_installed(res_mods_dir, requested):
            raise SystemExit(f"{requested} font files not found in {res_mods_dir}\\gui\\fonts")
        return requested
    if font_installed(res_mods_dir, "warhelios-east-asia"):
        return "warhelios-east-asia"
    return BUNDLED_FONT


def add_missing_glyphs(font, donor):
    """Copy every character of donor that font has no glyph for, scaled to font's em size."""
    font_cmap = font.getBestCmap()
    missing = {codepoint: name for codepoint, name in donor.getBestCmap().items()
               if codepoint not in font_cmap}
    scale = font["head"].unitsPerEm / donor["head"].unitsPerEm
    donor_glyphs = donor.getGlyphSet()
    glyf, hmtx = font["glyf"], font["hmtx"]
    glyph_order = font.getGlyphOrder()

    copied = {}
    for codepoint, donor_name in sorted(missing.items()):
        if donor_name not in copied:
            recording = DecomposingRecordingPen(donor_glyphs)
            donor_glyphs[donor_name].draw(recording)
            pen = TTGlyphPen(None)
            recording.replay(TransformPen(pen, (scale, 0, 0, scale, 0, 0)))
            glyph = pen.glyph()
            glyph.recalcBounds(glyf)

            name = "textmod." + donor_name
            glyph_order.append(name)
            glyf[name] = glyph
            hmtx[name] = (round(donor_glyphs[donor_name].width * scale), getattr(glyph, "xMin", 0))
            copied[donor_name] = name
        for table in font["cmap"].tables:
            if table.isUnicode() and (codepoint <= 0xFFFF or table.format in (12, 13)):
                table.cmap[codepoint] = copied[donor_name]
    font.setGlyphOrder(glyph_order)
    return len(missing)


def build_fonts(wows_dir, build_dir, res_mods_dir, font_key):
    """Write the patched regular and bold fonts; returns (regular name, path, bold name, path)."""
    result = []
    for base_path, stock_path, patched_path in zip(FONTS[font_key], STOCK_FONTS, PATCHED_FONTS):
        installed = os.path.join(res_mods_dir, base_path)
        if os.path.exists(installed):
            base = TTFont(installed)
        else:
            base = TTFont(io.BytesIO(read_packaged_file(wows_dir, build_dir, base_path)))
        stock = TTFont(io.BytesIO(read_packaged_file(wows_dir, build_dir, stock_path)))
        added = add_missing_glyphs(base, stock)
        base.save(os.path.join(res_mods_dir, patched_path))
        print(f"wrote {patched_path}: {os.path.basename(base_path)} + {added} glyphs from "
              f"{os.path.basename(stock_path)}")
        result += [base["name"].getDebugName(4), patched_path]
    return tuple(result)


def write_fontconfig(res_mods_dir, font):
    gui_dir = os.path.join(res_mods_dir, "gui")
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
    print(f"building font from {font_key}")
    os.makedirs(os.path.join(res_mods_dir, "gui", "fonts"), exist_ok=True)
    font = build_fonts(args.wows_dir, build_dir, res_mods_dir, font_key)
    write_fontconfig(res_mods_dir, font)
    print(f"wrote {res_mods_dir}\\gui\\fontconfig_*.xml")


if __name__ == "__main__":
    main()
