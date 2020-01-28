# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 18:03:31 2020

@author: AsteriskAmpersand
"""

from mrl3.MaterialMrl3 import MRL3 as BaseMrl3
from imrl3.MaterialMrl3 import MRL3 as IBMrl3
from common.FileLike import FileLike
from pathlib import Path
from copy import deepcopy
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


class MaterialCompatibilizer():
    def __init__(self,altList = []):
        self.loadMaterialTable()
        self.loadAlternatives(altList)
    
    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
            
    def loadMaterialTable(self):
        try:
            listPath = appPath(r"Master_MtList_i.mrl3")
        except:
            listPath = r"..\Master_MtList_i.mrl3"
        im = IBMrl3()
        with open(self.resource_path(listPath),"rb") as tFile:
            data = tFile.read()
            im.marshall(FileLike(data))
        self.masterTable = im
        self.hashMap = {entry.Header.shaderHash:entry for entry in reversed(im.Materials)}
        self.masterResources = im.Textures
            
    def loadAlternatives(self,alternativeList):
        self.altMap = {}
        self.altResources = {}
        for filename in alternativeList:
            try:
                m = BaseMrl3()
                with open(filename,"rb") as matfile:
                    m.marshall(FileLike(matfile.read()))
                for entry in m.Materials:
                    self.altMap[entry.Header.shaderHash] = entry
                    self.altResources[entry.Header.shaderHash] = m.Textures
            except:
                pass
        return
    
    ibunkn = [12,0,0,0, 42,102,7,93, 0,0,0,0]
    def compatibilize(self,materialPath):
        with open(materialPath,"rb") as mrl3File:
            m = BaseMrl3()
            m.marshall(FileLike(mrl3File.read()))
            if m.Header.unknArr == self.ibunkn:
                return
            resources = m.Textures
            self.updateHeader(m.Header)
            for i in range(len(m.Materials)):
                try:
                    m.Materials[i] = self.compatibilizeMaterial(resources,m.Materials[i])
                except:
                    #print("Error Updating %s"%materialPath + str(e))
                    raise
            m.updateCountsAndOffsets()
            newMat = m.serialize()
        with open(materialPath,"wb") as mrl3File:
            mrl3File.write(newMat)
            
            
    def updateHeader(self,header):
        header.headId = 0x4C524D
        header.unknArr = self.ibunkn
    
    def compatibilizeMaterial(self,newresources,material):
        matHash = material.Header.shaderHash
        try:
            newMat,oldresources = self.getMatch(matHash)
        except:
            raise ValueError("Material Hash not Found on Iceborne list.")
        self.updateMatHeader(material.Header,newMat.Header)
        self.updateBindings(material, newMat, oldresources,newresources)
        self.updateParameters(material,newMat)
        return newMat
    
    def updateMatHeader(self,materialHead,newMatHead):
        updateables = ["materialNameHash","unkn4","unkn5","unkn6","unkn7","unkn8"]
        #print("%X/%X"%(materialHead.materialNameHash,newMatHead.materialNameHash))
        for f in updateables:
            setattr(newMatHead,f,getattr(materialHead,f))
    
    def updateBindings(self,material, newMat, oldresources, newresources):
        typeMapping = {(b.resourceTypeName,b.mapTypeName) : b 
                   for b in material.resourceBindings}
        for binding in newMat.resourceBindings:
            if binding.resourceTypeName == "texture":
                if binding.mapTypeName == "Unknown Maptype":
                    raise ValueError("Updating requires usage of unknown resource binding.")
                key = (binding.resourceTypeName,binding.mapTypeName)
                if key in typeMapping:
                    binding.texIdx = typeMapping[key].texIdx
                else:
                    if oldresources[binding.texIdx] not in newresources:
                        newresources.append(oldresources[binding.texIdx-1])
                        binding.texIdx = len(newresources)

    def updateParameters(self,material, newMat):
        for paramArray in newMat.paramArray:
            if paramArray in material.paramArray:
                oldParamArray = material.paramArray.indexGet(paramArray)
                for field in oldParamArray.fields:
                    if "align" not in field:
                        if field in paramArray.fields:
                            if paramArray.fields[field] != oldParamArray.fields[field]:
                                for i,(l,r) in enumerate(zip(getattr(paramArray,field),getattr(oldParamArray,field))):
                                    getattr(paramArray,field)[i] = getattr(oldParamArray,field)[i]
                            else:
                                setattr(paramArray,field,getattr(oldParamArray,field))
            else:
                #print(type(paramArray).__name__)
                #print('\n'.join([type(p).__name__ for p in material.paramArray]))
                raise ValueError("Catastrophic Constant Buffer Corruption.")
        
    def getMatch(self,matHash):
        if matHash in self.hashMap:
            return deepcopy(self.hashMap[matHash]), self.masterResources
        else:
            return deepcopy(self.altMap[matHash]), self.altResources[matHash]