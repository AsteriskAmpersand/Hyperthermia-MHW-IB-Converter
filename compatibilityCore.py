# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:16:51 2020

@author: AsteriskAmpersand
"""

from compatibility.cclCompatibility import CclCompatibilizer as ccl
from compatibility.ctcCompatibility import CtcCompatibilizer as ctc
from compatibility.materialCompatibility import MaterialCompatibilizer as mrl3
from compatibility.evCompatibility import EVCompatibilizer as ev
class CompatibilityEngine():
    def __init__(self):
        self.mrl3 = mrl3()
        self.ctc = ctc()
        self.ccl = ccl()
        self.ev = ev()
        
    def detectType(self,filePath):
        return {".mrl3":self.mrl3,".ctc":self.ctc,".ccl":self.ccl,
                ".evwp":self.ev,".evhl":self.ev,".evbd":self.ev}[filePath.suffix]
    
    def convert(self,path):
        if path.is_dir():
            self.recursiveCompatibilize(path)
        else:
            self.compatibilize(path)
    
    def recursiveCompatibilize(self,root):
        for extension in ["*.mrl3","*.ctc","*.ccl","*.evwp","*.evhl","*.evbd"]:
            for file in root.rglob(extension):
                self.compatibilize(file)
    
    def compatibilize(self,filepath):
        print("Converting %s"%filepath)
        compatibilizer = self.detectType(filepath)
        compatibilizer.compatibilize(filepath)
        
if __name__== "__main__":
    from pathlib import Path
    import sys
    engine = CompatibilityEngine()
    if len(sys.argv)<2:
        print("Drag file or directory to update to Iceborne (visuals only).")
        path = Path(r"E:\IBProjects\ArmorPorts\Lightning - Copy")
        engine.convert(path)
    else:
        path = Path(sys.argv[1])
        engine.convert(path)
    