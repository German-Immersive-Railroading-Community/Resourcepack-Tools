import json
import os
import zipfile
import urllib.request as url
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except (ImportError, AttributeError):
    compression = zipfile.ZIP_STORED

if not os.path.exists("project.json"):
    with open("project.json", "w") as fp:
        jobj = {"name": input("Please enter your project name: ")}
        json.dump(jobj, fp)

fp = open("project.json")
projectJson = json.load(fp)
fp.close()

if not os.path.exists("project.mcmeta"):
    with open("project.mcmeta", "w") as fp:
        json.dump({"pack": {"pack_format": 3, "description": projectJson["name"] } }, fp)

def packAbleFiles(file):
    return file.endswith(".json") or file.endswith(".obj") or file.endswith(".png") or file.endswith(".mcmeta") or file.endswith(".mtl")


def pack():
    with zipfile.ZipFile(projectJson["name"] + ".zip", "w") as zf:
        for root, dirs, files in os.walk("."):
            for file in files:
                pth = os.path.join(root, file)
                if packAbleFiles(file):
                    if (os.path.sep + "models" + os.path.sep) in root and file.endswith(".png"):
                        zf.write(pth, compress_type=compression, arcname="assets/minecraft/textures/" + file)
                    else:
                        zf.write(pth, compress_type=compression)

def requ(cmd, data=None, mthd=None) -> dict:
    header = {}
    req = url.Request("https://api.github.com/repos/German-Immersive-Railroading-Community/GIRSignals/" + cmd, headers=header, method=mthd, data=data)
    with url.urlopen(req) as rsp:
        return json.load(rsp)

def update():
    rsp = requ("branches/master")
    rsp = requ("git/trees/" + rsp["commit"]["commit"]["tree"]["sha"])

    for nxt in ["src", "main", "resources", "assets", "girsignals"]:
        rsp = requ("git/trees/" + list(filter(lambda el: el["path"] == nxt, rsp["tree"]))[0]["sha"])
    print(rsp)


commands = { "update":update, "pack": pack }


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
        if type(numorcmd) == str:
            commands[numorcmd]()
        elif type(numorcmd) == int:
            (list(commands.values())[numorcmd])()
        clear()
    except(KeyError, IndexError):
        clear()
        print("Couldn't find command!")
