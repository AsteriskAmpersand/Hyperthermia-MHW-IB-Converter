# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 03:20:50 2019

@author: AsteriskAmpersand
"""
import sys
sys.path.append("..")

from collections import OrderedDict
from common.Cstruct import PyCStruct

    
class Header(PyCStruct):
    fields = OrderedDict([
    	("filetype", "char[4]"),#[CCL\x00]
    	("unknownHeaderBytes", "ubyte[4]"),#[24,6,8,0]
    	("numCCLRecords", "int"),
    	("capsuleBuffer", "int32"),#0x40*numCCLRecords
    ])
    
    def construct(self, recordCount):
        self.filetype = "CCL\x00"
        self.unknownHeaderBytes = [24,6,8,0]
        self.numCCLRecords = recordCount
        self.capsuleBuffer = 0x40*recordCount
        return self

class CCLRecords(PyCStruct):
    fields = OrderedDict([
	("zeroBytes", "byte[4]"),
	("boneIDOne", "short"),
	("boneIDTwo", "short"),
	("unknownFrontBytesCont", "byte[8]"),
	("startsphere_xOffset", "float"),
	("startsphere_yOffset", "float"),
	("startsphere_zOffset", "float"),
	("startsphere_radius", "float"),
	("endsphere_xOffset", "float"),
	("endsphere_yOffset", "float"),
	("endsphere_zOffset", "float"),
	("endsphere_radius", "float"),
    ("endZeroes", "byte[12]"),
	("unknownEndBytes", "byte[4]"),
    ])
    
    def construct(self, data):
        self.zeroBytes = [0,0,0,0]
        self.boneIDOne = data["boneIDOne"]
        self.boneIDTwo = data["boneIDTwo"]
        self.unknownFrontBytesCont = data["unknownBytes"][:8]
        startVector = data["startsphere"]
        endVector = data["endsphere"]
        self.startsphere_xOffset = startVector[0]
        self.startsphere_yOffset = startVector[1]
        self.startsphere_zOffset = startVector[2]
        self.startsphere_radius = data["startsphere_radius"]
        self.endsphere_xOffset = endVector[0]
        self.endsphere_yOffset = endVector[1]
        self.endsphere_zOffset = endVector[2]
        self.endsphere_radius = data["endsphere_radius"]
        self.endZeroes = [0]*12
        self.unknownEndBytes = data["unknownBytes"][8:]
        return self

class CCL():
    def marshall(self,data):
        self.Header = Header().marshall(data)
        self.Records = [CCLRecords().marshall(data) for record in range(self.Header.numCCLRecords)]
        return self
    def __iter__(self):
        return iter(self.Records)
    def serialize(self):
        return self.Header.serialize()+b''.join([record.serialize() for record in self.Records])
    def construct(self,data):
        records = data["Records"]
        self.Header = Header().construct(len(records))
        self.Records = records
        return self
        
"""
import numpy as np
from pathlib import Path
for path in Path(r"E:\MHW\Merged").rglob("*.ccl"):
    ccl = CclFile(path).data
    for record in ccl:
        print (str(record.unknownFrontBytesCont)+"-"+str(record.unknownEndBytes))
"""