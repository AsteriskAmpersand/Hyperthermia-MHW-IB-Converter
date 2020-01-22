# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 14:52:45 2020

@author: AsteriskAmpersand
"""
from col.Ccl import CCL
from common.FileLike import FileLike

class CclCompatibilizer():
    def compatibilize(self,cclPath):
        with open(cclPath,"rb") as cclFile:
            c = CCL()
            c.marshall(FileLike(cclFile.read()))
            self.updateCursedBytes(c)
        with open(cclPath,"wb") as cclFile:
            cclFile.write(c.serialize())
            
    def updateCursedBytes(self,cclData):
        for record in cclData.Records:
            for ix,i in enumerate(record.unknownFrontBytesCont):
                if ix>0:
                    if i == 0:
                        record.unknownFrontBytesCont[i] = -51
            for ix,i in enumerate(record.unknownEndBytes):
                if ix>11:
                    if i == 0:
                        record.unknownEndBytes[i] = -51       
                    