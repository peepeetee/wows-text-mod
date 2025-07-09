import os

import polib

import re 

import shutil

# wows_location = "C:\\Games\\World_of_Warships"
wows_location = "C:\Program Files (x86)\Steam\steamapps\common\World of Warships"


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




        entry.msgstr = re.sub( "Tang Sanzang", "唐三藏", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Zhu Bajie", "豬八戒", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Sha Wujing", "沙悟淨", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Sun Wukong", "孫悟空", entry.msgstr, re.IGNORECASE)


        entry.msgstr = re.sub( "Bajie", "八戒", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Wujing", "悟淨", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Wukong", "悟空", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Sanzang", "三藏", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Harbin", "哈爾濱", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Sejong", "世宗", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Huanghe", "黃河", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Dalian", "大連", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Fushun", "撫順", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Chung Mu", "忠武", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Anshan", "鞍山", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Sun Yat-Sen", "孫逸仙", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Yamato", "大和", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Kongō", "金剛", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Kirishima", "霧島", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Hiei", "比叡", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Haruna", "榛名", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Myōkō", "妙高", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Ashigara", "足柄", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Takao", "高雄", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Haguro", "羽黒", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Maya", "摩耶", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Nachi", "那智", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Xin Zhong Guo", "「新中國」", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Yamamoto Isoroku", "山本五十六", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Kunming", "昆明", entry.msgstr, re.IGNORECASE)

        entry.msgstr = re.sub( "Mengchong", "蒙衝", entry.msgstr, re.IGNORECASE)   
        entry.msgstr = re.sub( "Incheon", "仁川", entry.msgstr, re.IGNORECASE)  
        entry.msgstr = re.sub( "Louchuan", "樓船", entry.msgstr, re.IGNORECASE) 
        entry.msgstr = re.sub( "Tianjin", "天津", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Taihang", "太行", entry.msgstr, re.IGNORECASE)
        entry.msgstr = re.sub( "Lüshun", "旅順", entry.msgstr, re.IGNORECASE)




print("checking if directory exists\n")

if not os.path.exists(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES"):
    os.makedirs(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES")

if not os.path.exists(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES"):
    os.makedirs(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES")

print("writing global.mo\n")

output.save(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\en\\LC_MESSAGES\\global.mo")
output.save(wows_location + "\\bin\\" + wows_version + "\\res_mods\\texts\\ja\\LC_MESSAGES\\global.mo")


print("copying fontconfig.xml\n")

# directory = os.path.realpath()

shutil.copyfile("D:\\WOWS fuckery\\fontconfig.xml", wows_location + "\\bin\\" + wows_version + "\\res_mods\\fontconfig.xml")
# shutil.copyfile(directory + "\\fontconfig.xml", wows_location + "\\bin\\" + wows_version + "\\res_mods\\fontconfig.xml")
