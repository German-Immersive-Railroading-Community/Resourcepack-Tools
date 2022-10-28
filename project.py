import json
import os
import zipfile
import urllib.request as url
import re
import traceback
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except (ImportError, AttributeError):
    compression = zipfile.ZIP_STORED

first = False

if not os.path.exists("project.json"):
    first = True
    with open("project.json", "w") as fp:
        jobj = {"name": input("Please enter your project name: ")}
        json.dump(jobj, fp)

fp = open("project.json")
projectJson = json.load(fp)
fp.close()


def save():
    with open("project.json", "w") as fp:
        json.dump(projectJson, fp)


if not os.path.exists("pack.mcmeta"):
    with open("pack.mcmeta", "w") as fp:
        json.dump(
            {"pack": {"pack_format": 3, "description": projectJson["name"]}}, fp)


def packAbleFiles(file):
    return file.endswith(".json") or file.endswith(".obj") or file.endswith(".png") or file.endswith(".mcmeta") or file.endswith(".mtl")


depCache = None
ptrn = r"\s*cm\.register\s*\(\s*\"([^\"]+)\",((.*\),)|([^\,]+,))\s*[0-9\.f]*,([^\)]+)\)\;"
ptrn2 = r"\s*\"([^\"]+)\""


def check(name, pth):
    global depCache
    try:
        if depCache == None:
            depCache = []
            with open("GIRCustomModelLoader.java") as fp:
                groups1 = re.findall(ptrn, fp.read())
                for cont in groups1:
                    name = cont[0]
                    name = os.path.basename(name) + ".json"
                    if len(cont) == 5:
                        scre = cont[4]
                        rslt = re.findall(ptrn2, scre)
                        depCache.append((name, rslt))
        cacheLists = list(filter(lambda x: x[0] == name, depCache))
        if len(cacheLists) > 0:
            with open(pth) as fp:
                jobj = json.load(fp)
                if "textures" not in jobj:
                    return
                texlist = jobj["textures"]
                dupl = []
                for tpl in cacheLists:
                    lst = tpl[1]
                    for x in range(0, len(lst), 2):
                        if lst[x] not in texlist:
                            if lst[x] in dupl: continue
                            dupl.append(lst[x])
                            print("Warning {} not found in texture list of {}, please make sure it uses this texture as it is needed! [Example: {}]".format(
                                lst[x], name, lst[x+1]))
    except:
        traceback.print_exc()
        print("Error in cmd!")


def pack():
    vers = "none"
    if "version" not in projectJson:
        print("Warning no version provided! Use update to get the data structure from the most recent version!")
    else:
        vers = projectJson["version"]
    with zipfile.ZipFile(projectJson["name"] + " for OpenSignals " + vers + ".zip", "w") as zf:
        for root, dirs, files in os.walk("."):
            for file in files:
                pth = os.path.join(root, file)
                if packAbleFiles(file):
                    check(file, pth)
                    if (os.path.sep + "models" + os.path.sep) in root and file.endswith(".png"):
                        zf.write(pth, compress_type=compression,
                                 arcname="assets/minecraft/textures/" + file)
                    else:
                        zf.write(pth, compress_type=compression)


def requ(cmd, data=None, mthd=None) -> dict:
    header = {}
    req = url.Request("https://api.github.com/repos/MrTroble/Open-Signals" +
                      cmd, headers=header, method=mthd, data=data)
    with url.urlopen(req) as rsp:
        return json.load(rsp)


def update():
    rsp = requ("releases")
    version = rsp[0]["name"]
    if "version" in projectJson and projectJson["version"] == version:
        print("Version up to date!")
        return
    rsp = url.urlopen(rsp[0]["zipball_url"])
    with open("dl.zip", "wb") as fp:
        fp.write(rsp.read())
    for root, dir, files in os.walk("assets"):
        for file in files:
            pth = os.path.join(root, file)
            if pth.endswith(".dummy"):
                os.remove(pth)

    with zipfile.ZipFile("dl.zip") as zf:
        for zi in zf.filelist:
            if zi.filename.endswith("GIRCustomModelLoader.java"):
                with zf.open(zi, "r") as zfp:
                    with open("GIRCustomModelLoader.java", "wb") as nfp:
                        nfp.write(zfp.read())
            if "/src/main/resources/assets/" in zi.filename:
                fname = zi.filename.split("/src/main/resources/")[1]
                if zi.is_dir():
                    if not os.path.exists(fname):
                        os.makedirs(fname)
                    continue
                with zf.open(zi, "r") as zfp:
                    with open(fname + ".dummy", "wb") as nfp:
                        nfp.write(zfp.read())
    projectJson["version"] = version
    save()
    os.remove("dl.zip")


if first:
    update()

def checkAll():
    for root, dirs, files in os.walk("."):
        for file in files:
            if packAbleFiles(file):
                pth = os.path.join(root, file)
                check(file, pth)

def checkcmd():
    name = input("Filename: ")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == name:
                pth = os.path.join(root, file)
                check(file, pth)

commands = {"update": update, "pack": pack, "checkall": checkAll, "check": checkcmd }


def clear(): os.system("cls")


while True:
    print("""
====================================================

            OPEN SIGNAL RP PROJECT TOOL

====================================================
    """)

    for num, cmd in enumerate(commands.keys()):
        print(str(num) + ". " + cmd)

    numorcmd = input()
    try:
        numorcmd = int(numorcmd)
    except:
        pass
    try:
        clear()
        if type(numorcmd) == str:
            commands[numorcmd]()
        elif type(numorcmd) == int:
            (list(commands.values())[numorcmd])()
    except(KeyError, IndexError):
        clear()
        print("Couldn't find command!")
