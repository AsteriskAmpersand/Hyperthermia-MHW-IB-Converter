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
    def __init__(self,decider = None,inputHandler = None, output = print):
        self.mrl3 = mrl3()
        self.ctc = ctc()
        self.ccl = ccl()
        self.ev = ev(decider,inputHandler)
        self.output = output
        
    def detectType(self,filePath):
        return {".mrl3":self.mrl3,".ctc":self.ctc,".ccl":self.ccl,
                ".evwp":self.ev,".evhl":self.ev,".evbd":self.ev}[filePath.suffix]
    
    def convert(self,path,debug):
        if path.is_dir():
            self.recursiveCompatibilize(path,debug)
        else:
            self.compatibilize(path,debug)
    
    def recursiveCompatibilize(self,root,debug):
        for extension in ["*.mrl3","*.ctc","*.ccl","*.evwp","*.evhl","*.evbd"]:
            for file in root.rglob(extension):
                self.compatibilize(file, debug)
    
    def compatibilize(self,filepath,debug):
        self.output("Converting %s"%filepath)
        compatibilizer = self.detectType(filepath)
        try:
            compatibilizer.compatibilize(filepath)
        except Exception as e:
            if not(debug):
                self.output("Error compatibilizing %s. Skipped."%filepath)
            else:
                self.output("Error compatibilizing %s. Error:\n%s"%(filepath,e))
                
if __name__== "__main__":
    from pathlib import Path
    import sys
    debug = True#False
    if len(sys.argv)<2:
        path = Path(input("Drag file or directory to update to Iceborne (visuals only).\n").replace('"',"").replace("'",""))
    else:
        if len(sys.argv)>2:
            if sys.argv[2] == "--debug":
                debug = True
        path = Path(sys.argv[1])
    engine = CompatibilityEngine()
    engine.convert(path, debug)
    input("Conversion Process Completed.")
        
    
