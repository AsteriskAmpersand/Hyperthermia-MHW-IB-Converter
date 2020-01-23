# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 02:06:55 2020

@author: AsteriskAmpersand
"""
from pathlib import Path
import sys
import os

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

oldChunk = appPath(r"evxx_resources\base")
newChunk = appPath(r"evxx_resources\ib")

class EVGenericCompatibilizer():
    oroot = oldChunk
    iroot = newChunk
    def __init__(self,*args):
        self.oldNewMap = self.loadSuffixTable(self.oroot, self.iroot)
    def binaryCompatibilize(self,path):
        with path.open("rb") as df:
            data = df.read()
        for file in self.oldNewMap:
            with file.open("rb") as candidate:
                match = self.binaryMatch(data,candidate.read())
                if match:
                    return self.oldNewMap[file]
        return self.defaultCompatibilize(path,None)
    def compatibilize(self,path,default = None):
        if default is None:
            cpath = self.binaryCompatibilize(path)
        else:
            cpath = self.defaultCompatibilize(path,default)
        with path.open("wb") as of:
            with cpath.open("rb") as inf:
                of.write(inf.read())        
    def loadSuffixTable(self, oroot = oldChunk, iroot = newChunk):
        table = {}
        for oldPath in oroot.rglob(self.suffixRegex):
            newPath = iroot.joinpath(str(oldPath.relative_to(oroot)))
            table[oldPath] = newPath
        return table
    def binaryMatch(self,old,new):
        for l,r in zip(old,new):
            if l!=r:
                return False
        return True
    
class WeaponCompatibilizer(EVGenericCompatibilizer):
    suffixRegex = "*.evwp"
    def __init__(self, wp):
        self.wp = wp
        self.oroot = appPath(r"evxx_resources\base\wp\%s"%self.wp)
        self.iroot = appPath(r"evxx_resources\ib\wp\%s"%self.wp)
        super().__init__()
    def defaultCompatibilize(self,path,default):
        subtype = path.stem[:-3]
        if "_" in subtype:
            subtype = subtype[subtype.index("_")+1:]
        return self.iroot.joinpath("%s001\mod\%s001.evwp"%(self.wp,subtype))
    
weaponList = ["bow","caxe","gun","ham","hbg","hue","lan","lbg","mus","one",
              "saxe","sou","swo","two"]

armoryCompatibilizer = { wp:WeaponCompatibilizer(wp) for wp in weaponList }
    
class BodyCompatibilizer(EVGenericCompatibilizer):
    suffixRegex = "*.evbd"
    defaultbodyf = appPath(r"evxx_resources\ib\pl\f_equip\pl001_0000\body\mod\f_body001_0000.evbd")
    defaultbodym = appPath(r"evxx_resources\ib\pl\m_equip\pl001_0000\body\mod\m_body001_0000.evbd")
    def __init__(self, g):
        self.oroot = appPath(r"evxx_resources\base\pl\%s_equip"%g)
        self.iroot = appPath(r"evxx_resources\ib\pl\%s_equip"%g)
        self.gender = g
        super().__init__()
    def defaultCompatibilize(self,path,default):
        return self.defaultbodyf if self.gender == "f" else self.defaultbodym 
bodies = {"m":BodyCompatibilizer("m"),"f":BodyCompatibilizer("f")}
class HeadCompatibilizer(EVGenericCompatibilizer):
    suffixRegex = "*.evhl"
    hollow = appPath(r"evxx_resources\f_helmXXX_0000.evhl")
    fullhairf = appPath(r"evxx_resources\ib\pl\f_equip\pl063_0000\helm\mod\f_helm063_0000.evhl")
    fullhairm = appPath(r"evxx_resources\ib\pl\m_equip\pl063_0000\helm\mod\m_helm063_0000.evhl")
    def __init__(self, g):
        self.oroot = appPath(r"evxx_resources\base\pl\%s_equip"%g)
        self.iroot = appPath(r"evxx_resources\ib\pl\%s_equip"%g)
        self.gender = g
        super().__init__()
    def defaultCompatibilize(self,path,default):
        if default == "H":
            return self.hollow
        else:
            return self.fullhairf if self.gender == "f" else self.fullhairm
heads = {"m":HeadCompatibilizer("m"),"f":HeadCompatibilizer("f")}

class EVCompatibilizer():
    def __init__(self,decider = None, caller = None):
        if not decider:
            while True:
                try:
                    self.body = {"D":"Default","C":"Input","S":None}[input("Use [D]efault Body, [S]earch Match or [C]ase by Case Basis for EVBD?: ").upper()]
                    self.head = {"H":"H","F":"F","C":"Input","S":None}[input("Use [H]ollow Head, [F]ull Hair, [S]earch Match or [C]ase by Case Basis for EVHL?: ").upper()]
                    self.weapons = {"D":"Default","C":"Input","S":None}[input("Use [D]efault Weapon Position, [S]earch Match or [C]ase by Case Basis for EVWP?: ").upper()]
                    break
                except:
                    pass
                def bodyInput(path): return input("Use Default Body EVBD for %s: [Y|N]"%path).upper()=="Y"
                self.bodyInput = staticmethod(bodyInput)
                def weaponInput(path): return input("Use Default Weapon EVWP for %s: [Y|N]"%path).upper()=="Y"
                self.weaponInput = staticmethod(weaponInput)
                def headInput(path): input("Use [H]ollow Head/[F]ull Hair/[S]earch for Match for EVHL for %s:"%path).upper()
                self.headInput = staticmethod(headInput)
        else:
            self.body = decider["Body"]
            self.head = decider["Head"]
            self.weapons = decider["Weapons"]
            self.bodyInput = caller["Body"]
            self.weaponInput = caller["Weapons"]
            self.headInput = caller["Head"]
        
    def compatibilize(self,path):
        if bytearray(path.open("rb").read(4)) == bytearray([0x01, 0x10, 0x09, 0x18]):
            return
        suffix = path.suffix
        if ".evwp" in suffix:
            for wp in weaponList:
                if wp in path.stem:
                    armoryCompatibilizer[wp].compatibilize(path,self.decide(path,"Weapons"))
        if ".evbd" in suffix:
            g = self.getGender(path)
            bodies[g].compatibilize(path,self.decide(path,"Body"))     
        if ".evhl" in suffix:
            g = self.getGender(path)
            heads[g].compatibilize(path,self.decide(path,"Head"))
    def getGender(self,path):
        if "m_" in path.stem:
            g = "m"
        else:
            g = "f"
        return (g)
    def decide(self,path, typing):
        if typing == "Body":
            if self.body == "Input":
                return True if self.bodyInput(path) else None
            return True if self.body == "Default" else None
        if typing == "Weapons":
            if self.weapons == "Input":
                return True if self.weaponInput(path) else None
            return True if self.weapons == "Default" else None
        if typing == "Head":
            if self.head == "Input":
                dec = self.headInput(path)
            else:
                dec = self.head
            if dec == "S":
                return None
            else:
                return dec

