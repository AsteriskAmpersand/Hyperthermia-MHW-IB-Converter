# -*- coding: utf-8 -*-

from collections import OrderedDict
from common.Cstruct import PyCStruct
from common.FileLike import FileLike

class WpDatHeader(PyCStruct):
    fields = OrderedDict([
    ("signature","uint16"),#0x0186
    ("num_entries","uint32")
    ])

class WpDatEntry(PyCStruct):
    fields = OrderedDict([
    ("entry_index", "uint32"),
    ("unknown1", "byte"),
    ("unknown2","byte"),
    ("base_model_id", "uint16"),
    ("part1_id", "uint16"),
    ("part2_id", "uint16"),
    ("unknown3", "ubyte[53]")
    ])
    
class WpDatGEntry(PyCStruct):
    fields = OrderedDict([
    ("entry_index", "uint32"),
    ("unknown1", "byte"),
    ("unknown2","byte"),
    ("base_model_id", "uint16"),
    ("part1_id", "uint16"),
    ("part2_id", "uint16"),
    ("unknown3", "ubyte[56]")
    ])
    
class iWpDatHeader(PyCStruct):
    fields = OrderedDict([
	("ibsig","byte[4]"),
    ("signature","uint16"),#0x0186
    ("num_entries","uint32")
    ])
    
class iWpDatEntry(PyCStruct):
    fields = OrderedDict([
    ("entry_index", "uint32"),
    ("unknown1", "byte"),
    ("unknown2","byte"),
    ("base_model_id", "uint16"),
    ("part1_id", "uint16"),
    ("part2_id", "uint16"),
    ("unknown3", "ubyte[54]")
    ])
    
class iWpDatGEntry(PyCStruct):
    fields = OrderedDict([
    ("entry_index", "uint32"),
    ("unknown1", "byte"),
    ("unknown2","byte"),
    ("base_model_id", "uint16"),
    ("part1_id", "uint16"),
    ("part2_id", "uint16"),
    ("unknown3", "ubyte[57]")
    ])

class WpDat():
    header = WpDatHeader
    def __init__(self,path = None):
        if path is not None:
            with open(path,"rb") as inf:
                self.marshall(FileLike(inf.read()))
    def marshall(self, data):
        self.Header = self.header().marshall(data)
        self.Entries = [self.datEntry().marshall(data) for _ in range(self.Header.num_entries)]
        return self
    def __getitem__(self, index):
        #entry = self.Entries[index]
        return self.Entries[index]#(entry.base_model_id, entry.part1_id, entry.part2_id)
    def __iter__(self):
        return iter(self.Entries)
    def serialize(self):
        return self.Header.serialize()+b''.join(map(lambda x: x.serialize(),self.Entries))

class iWpDat(WpDat):
    header = iWpDatHeader


class MeleeDat(WpDat):
    datEntry = WpDatEntry
class GunnerDat(WpDat):
    datEntry = WpDatGEntry
class iMeleeDat(iWpDat):
    datEntry = iWpDatEntry
class iGunnerDat(iWpDat):
    datEntry = iWpDatGEntry