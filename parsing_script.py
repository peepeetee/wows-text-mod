import os

import polib

import re 

import shutil

# wows_location = "C:\\Games\\World_of_Warships"
wows_location = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\World of Warships"


#wows_version = "6359964"

wows_version = max(os.listdir(wows_location + "\\bin"),key=int)

# wows_version = "9531281"


print("wows location: " + wows_location + "\\bin\\" + wows_version + "\n")


output = polib.MOFile()

en_location = (wows_location + "\\bin\\" + wows_version + "\\res\\texts\\en\\LC_MESSAGES\\global.mo")
ja_location = (wows_location + "\\bin\\" + wows_version + "\\res\\texts\\ja\\LC_MESSAGES\\global.mo")
zh_location = (wows_location + "\\bin\\" + wows_version + "\\res\\texts\\zh_tw\\LC_MESSAGES\\global.mo")
ru_location = (wows_location + "\\bin\\" + wows_version + "\\res\\texts\\ru\\LC_MESSAGES\\global.mo")


en = polib.mofile(en_location, encoding='utf-8')
ja = polib.mofile(ja_location, encoding='utf-8')
zh = polib.mofile(zh_location, encoding='utf-8')
ru = polib.mofile(ru_location, encoding='utf-8')

output.metadata = en.metadata

print("parsing with regex\n")

for entry in en:


    if re.search("^IDS_PJ[A-Z][A-Z][0-9][0-9][0-9]", entry.msgid):
        output.append(ja.find(entry.msgid))

    elif re.search(".*JAPAN.*", entry.msgid):
        output.append(ja.find(entry.msgid))
    elif re.search("^IDS_PR[A-Z][A-Z][0-9][0-9][0-9]", entry.msgid):
        output.append(ru.find(entry.msgid))
    elif re.search(".*RUSSIA.*", entry.msgid):
        output.append(ru.find(entry.msgid))

    elif re.search("^IDS_PZ[A-Z][A-Z][0-9][0-9][0-9]", entry.msgid):
        output.append(zh.find(entry.msgid))
    elif re.search(".*PAN_ASIA.*", entry.msgid):
        output.append(zh.find(entry.msgid))
    else :
        output.append(entry)


print("parsing edge cases\n")

for entry in output:




        entry.msgstr = re.sub( pattern = "Tang Sanzang", repl = "唐三藏", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Zhu Bajie", repl = "豬八戒", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Sha Wujing", repl = "沙悟淨", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Sun Wukong", repl = "孫悟空", string = entry.msgstr, flags = re.IGNORECASE, count = 0)


        entry.msgstr = re.sub( pattern = "Bajie", repl = "八戒", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Wujing", repl = "悟淨", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Wukong", repl = "悟空", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Sanzang", repl = "三藏", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Harbin", repl = "哈爾濱", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Sejong", repl = "世宗", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Huanghe", repl = "黃河", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Dalian", repl = "大連", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Fushun", repl = "撫順", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Chung Mu", repl = "忠武", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Anshan", repl = "鞍山", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Sun Yat-Sen", repl = "孫逸仙", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Yamato", repl = "大和", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Kongō", repl = "金剛", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Kirishima", repl = "霧島", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Hiei", repl = "比叡", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Haruna", repl = "榛名", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Myōkō", repl = "妙高", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Ashigara", repl = "足柄", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Maya", repl = "摩耶", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Nachi", repl = "那智", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Xin Zhong Guo", repl = "「新中國」", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Yamamoto Isoroku", repl = "山本五十六", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Kunming", repl = "昆明", string = entry.msgstr, flags = re.IGNORECASE, count = 0)

        entry.msgstr = re.sub( pattern = "Mengchong", repl = "蒙衝", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Incheon", repl = "仁川", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Louchuan", repl = "樓船", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Tianjin", repl = "天津", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Taihang", repl = "太行", string = entry.msgstr, flags = re.IGNORECASE, count = 0)
        entry.msgstr = re.sub( pattern = "Lüshun", repl = "旅順", string = entry.msgstr, flags = re.IGNORECASE, count = 0)




print("checking if directory exists\n")

if not os.path.exists(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES"):
    os.makedirs(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES")

if not os.path.exists(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES"):
    os.makedirs(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES")

print("writing global.mo\n")

output.save(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES\\global.mo")
output.save(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES\\global.mo")


# print("copying fontconfig.xml\n")

# directory = os.path.realpath()

# shutil.copyfile("D:\\WOWS fuckery\\fontconfig.xml", wows_location + "\\bin\\" + wows_version + "\\res_mods\\fontconfig.xml")
# shutil.copyfile(directory + "\\fontconfig.xml", wows_location + "\\bin\\" + wows_version + "\\res_mods\\fontconfig.xml")
