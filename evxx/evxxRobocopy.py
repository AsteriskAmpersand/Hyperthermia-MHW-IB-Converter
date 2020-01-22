# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 01:45:58 2020

@author: AsteriskAmpersand
"""
from pathlib import Path

def zeroTrim(binaryFile):
    for ix,val in enumerate(reversed(binaryFile)):
        if val != 0:
            break
    return binaryFile[:-ix]

newchunk = Path(r"E:\MHW\chunkG0")
oldchunk = Path(r"E:\MHW\Merged")

base = Path(r"E:\IBProjects\ArmorPorts\LabComparison\IBConverter\evxx_resources\base")
iceborne = Path(r"E:\IBProjects\ArmorPorts\LabComparison\IBConverter\evxx_resources\ib")

suffixSet = {'.evwp':{}, '.evbd':{}, '.evhl':{}}

for oldPath in oldchunk.rglob("*.ev*"):
    suffix = oldPath.suffix
    if suffix not in suffixSet:
        continue
    newPath = newchunk.joinpath(str(oldPath.relative_to(oldchunk)))
    try:
        newPath.open("rb").read()
    except:
        continue
    basePath = base.joinpath(oldPath.relative_to(oldchunk))
    icebPath = iceborne.joinpath(newPath.relative_to(newchunk))
    basePath.parent.mkdir(parents=True, exist_ok=True)
    icebPath.parent.mkdir(parents=True, exist_ok=True)
    basePath.open("wb").write(zeroTrim(oldPath.open("rb").read()))
    icebPath.open("wb").write(newPath.open("rb").read())   