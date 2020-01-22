o# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 00:26:33 2020

@author: AsteriskAmpersand
"""
from itertools import chain
from pathlib import Path

IBBytes = bytearray([0x01, 0x10, 0x09, 0x18])
suffixSet = {'.evwp':{}, '.evbd':{}, '.evhl':{}}
newchunk = Path(r"E:\MHW\chunkG0")
oldchunk = Path(r"E:\MHW\Merged")
for oldPath in oldchunk.rglob("*.ev*"):
    suffix = oldPath.suffix
    if suffix not in suffixSet:
        continue
    newPath = newchunk.joinpath(str(oldPath.relative_to(oldchunk)))
    oldEvwp = IBBytes + bytearray(oldPath.open("rb").read())
    try:
        newEvwp = bytearray(newPath.open("rb").read())
    except:
        print("No file in Iceborne for %s"%oldPath)
        continue
    oldEvwp[8] = newEvwp[8]
    for ix,(l,r) in enumerate(zip(oldEvwp,newEvwp)):
        if l!=r:
            #print("%X %X"%(l,r))
            wx = len(newEvwp)-ix
            wx = ix
            if wx not in suffixSet[suffix]:
                suffixSet[suffix][wx] = []
            suffixSet[suffix][wx].append((len(newEvwp),newPath))
            break
for suffix in suffixSet:
    print("%s:"%suffix)
    dismatchIndex = suffixSet[suffix]
    for index in sorted(dismatchIndex.keys()):
        print("\t%d:"%index)
        for l,path in dismatchIndex[index]:
            print("\t\t%03d: %s"%(l,path))
            
#evbd are just truncated