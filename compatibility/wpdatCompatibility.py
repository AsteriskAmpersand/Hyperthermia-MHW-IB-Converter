# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:41:00 2020

@author: AsteriskAmpersand
"""

import os
import sys
from pathlib import Path
from dat.wp_dat import GunnerDat, MeleeDat, iGunnerDat, iMeleeDat
def appPath(path):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # Inside Exe: path into variable _MEIPASS'.
        # Outside Exe: os.path.dirname(sys.executable)
        application_path = Path(sys._MEIPASS)#os.path.dirname(sys.executable)
    elif __file__:
        application_path = Path(os.path.dirname(os.path.dirname(__file__)))
    return application_path.joinpath(path)

oldChunk = appPath(r"wp_resources\base")
newChunk = appPath(r"wp_resources\ib")

class GenericWpCompatibilizer():
    def __init__(self, wp):
        self.wp = wp
        self.basePath = appPath(oldChunk.joinpath(wp+(".wp_dat_g" if wp in gunner else ".wp_dat")))
        self.ibPath = appPath(newChunk.joinpath(wp+(".wp_dat_g" if wp in gunner else ".wp_dat")))
        self.parser = GunnerDat if wp in gunner else MeleeDat
        self.iparser = iGunnerDat  if wp in gunner else iMeleeDat
        self.base = self.parser(self.basePath)
        super().__init__()
    def loadConversionTable(self, base,ib):
        baseTable = {entry.entry_index : entry for entry in base}
        ibTable = {entry.entry_index : entry for entry in ib}
        return {entry:ibTable[entry] for entry in baseTable if entry in ibTable}
    def compatibilize(self,newdat):
        base = self.base
        ib = self.iparser(self.ibPath)
        table = self.loadConversionTable(base,ib)
        if not self.check(newdat):
            return
        newdatData = self.parser(newdat)
        for entry in newdatData:
            if entry.entry_index in table:
                self.mergeEntry(entry,table[entry.entry_index])
        with open(newdat,"wb") as outf:
            outf.write(ib.serialize())
    def check(self,filepath):
        with open(filepath,"rb") as inf:
            return not(bytearray(inf.read(4)) == bytearray([0x01, 0x10, 0x09, 0x18]))
                
    def mergeEntry(self,left,right):
        right.base_model_id = left.base_model_id
        right.part1_id = left.part1_id
        right.part2_id = left.part2_id
        return
    
blademaster = ["c_axe","g_lance","hammer","l_sword","lance","rod","s_axe","sword",
               "tachi","w_sword","whistle"]
gunner = ["bow","hbg","lbg"]

arsenal = {weapon:GenericWpCompatibilizer(weapon) for weapon in blademaster+gunner}

class WpDatCompatibilizer():
    def compatibilize(self,path):
        for wp in blademaster+gunner:
            if wp in path.stem:
                converter = arsenal[wp]
                break
        converter.compatibilize(path)
        return