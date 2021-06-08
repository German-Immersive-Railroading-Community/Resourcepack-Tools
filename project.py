import json
import os
import zipfile
import urllib.request as url
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


if not os.path.exists("project.mcmeta"):
    with open("project.mcmeta", "w") as fp:
        json.dump(
            {"pack": {"pack_format": 3, "description": projectJson["name"]}}, fp)


def packAbleFiles(file):
    return file.endswith(".json") or file.endswith(".obj") or file.endswith(".png") or file.endswith(".mcmeta") or file.endswith(".mtl")


def pack():
    vers = "none"
    if "version" not in projectJson:
        print("Warning no version provided! Use update to get the data structure from the most recent version!")
    else:
        vers = projectJson["version"]
    with zipfile.ZipFile(projectJson["name"] + " for GIRSignals " + vers + ".zip", "w") as zf:
        for root, dirs, files in os.walk("."):
            for file in files:
                pth = os.path.join(root, file)
                if packAbleFiles(file):
                    if (os.path.sep + "models" + os.path.sep) in root and file.endswith(".png"):
                        zf.write(pth, compress_type=compression,
                                 arcname="assets/minecraft/textures/" + file)
                    else:
                        zf.write(pth, compress_type=compression)


def requ(cmd, data=None, mthd=None) -> dict:
    header = {}
    req = url.Request("https://api.github.com/repos/German-Immersive-Railroading-Community/GIRSignals/" +
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


if first:
    update()

commands = {"update": update, "pack": pack}


def clear(): os.system("cls")


while True:
    print("""
====================================================

            GIR SIGNAL RP PROJECT TOOL

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
