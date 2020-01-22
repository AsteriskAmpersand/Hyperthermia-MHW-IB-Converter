# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:01:55 2020

@author: AsteriskAmpersand
"""
from col.Ctc import Ctc
from common.FileLike import FileLike

class CtcCompatibilizer():
    def compatibilize(self,ctcPath):
        with open(ctcPath,"rb") as ctcFile:
            data = ctcFile.read()
            if data[5] == b'\x1C':
                return
            c = Ctc()
            c.marshall(FileLike(data))
            self.updateCtc(c)
        with open(ctcPath,"wb") as ctcFile:
            ctcFile.write(c.serialize())
            
    def updateCtc(self,c):
        c.ibExpand()