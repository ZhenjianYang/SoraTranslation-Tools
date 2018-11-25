
from SoraFont import NO2SJIS, SJIS2NO, NUM_HALFWIDTH
from ChList import ChList
BASE_CODEC = 'ms932'


class CodeTable:
    def __init__(self):
        self.fixed = set()
        self.no2ucs = [0] * len(NO2SJIS)
        self.ucs2no = {}

        for i in range(len(NO2SJIS)):
            sjis = NO2SJIS[i]
            bs = bytearray()
            if sjis >= 0x8000:
                bs.append(sjis >> 8)
            bs.append(sjis & 0xFF)
            try: bs.decode(BASE_CODEC)
            except: self.fixed.add(i)
        
        self.idx_h = 0
        self.idx = NUM_HALFWIDTH
        self.added = [0] * len(NO2SJIS)
    
    def add_fixed_sjis(self, sjis, ucs=None):
        if sjis not in SJIS2NO:
            print('Warning: not a valid SJIS code: {0:X}'.format(sjis))
            return 0
        i = SJIS2NO[sjis]
        if ucs == None:
            bs = bytearray()
            if sjis >= 0x8000:
                bs.append(sjis >> 8)
            bs.append(sjis & 0xFF)
            ucs = ord(bs.decode(BASE_CODEC))
        elif type(ucs) is str:
            ucs = ord(ucs)
            
        self.fixed.add(i)
        self.no2ucs[i] = ucs
        self.ucs2no[ucs] = i
        return ucs
    
    def add_fixed(self, chlist_filename):
        chlist = ChList(BASE_CODEC, chlist_filename)
        for ch in chlist:
            sjis = 0
            for b in ch.code: sjis = (sjis << 8) | b
            if sjis not in SJIS2NO:
                print('Warning: not a valid SJIS code: {0:X}'.format(sjis))
                continue
            i = SJIS2NO[sjis]
            self.fixed.add(i)
            self.no2ucs[i] = ord(ch.glyph) if type(ch.glyph) is str else ch.glyph
            self.ucs2no[self.no2ucs[i]] = i
    
    def add(self, char, half=False):
        ucs = ord(char) if type(char) is str else char
        if ucs in self.ucs2no:
            idx = self.ucs2no[ucs]
            self.added[idx] = ucs
            return idx

        if half:
            while self.no2ucs[self.idx_h] or self.idx_h in self.fixed:
                self.idx_h += 1
            if self.idx_h >= NUM_HALFWIDTH:
                raise('No enouth space for halfwidth charactors!')
            self.no2ucs[self.idx_h] = ucs
            self.ucs2no[ucs] = self.idx_h
            self.added[self.idx_h] = ucs
            self.idx_h += 1
            return self.idx_h
        else:
            while self.no2ucs[self.idx] or self.idx in self.fixed:
                self.idx += 1
            if self.idx >= len(self.no2ucs):
                raise('No enouth space for more charactors!')
            self.no2ucs[self.idx] = ucs
            self.ucs2no[ucs] = self.idx
            self.added[self.idx] = ucs
            self.idx += 1
            return self.idx - 1
    
    def get_added_list(self):
        added_list = []
        for i, ucs in enumerate(self.added):
            if ucs:
                added_list.append([NO2SJIS[i], ucs])
        return added_list
    
    def get_fixed_list(self):
        fixed_list = []
        for i in sorted(self.fixed):
            if self.no2ucs[i]:
                fixed_list.append([NO2SJIS[i], self.no2ucs[i]])
        return fixed_list
