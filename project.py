import json
import os
import zipfile
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


def packAbleFiles(file):
    return file.endswith(".json") or file.endswith(".obj") or file.endswith(".png") or file.endswith(".mcmeta") or file.endswith(".mtl")


def pack():
    with zipfile.ZipFile(projectJson["name"] + ".zip", "w") as zf:
        for root, dirs, files in os.walk("."):
            for file in files:
                pth = os.path.join(root, file)
                if packAbleFiles(file):
                    zf.write(pth, compress_type=compression)


commands = {"pack": pack }


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
