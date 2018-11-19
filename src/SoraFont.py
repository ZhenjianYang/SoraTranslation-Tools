import struct

NUM_HALFWIDTH = 16 * 12

SJIS_RANGE_SIGLE_BYTE = [[0x20, 0xDF]]
SJIS_RANGE_DOUBLE_BYTES = [[0x8140, 0x81F7], [0x8240, 0x82F1], [0x8340, 0x83D6], [0x8440, 0x84BE], [0x8740, 0x879C], [0x889F, 0x9FFC], [0xE040, 0xEAA5]]

NO2SJIS = []
SJIS2NO = {}

def _init_map():
    for l, h in SJIS_RANGE_SIGLE_BYTE + SJIS_RANGE_DOUBLE_BYTES:
        for code in range(l, h+1):
            if code >= 0x8000 and not 0x40 <= (code & 0xFF) <= 0xFC:
                continue
            SJIS2NO[code] = len(NO2SJIS)
            NO2SJIS.append(code)

_init_map()

class SoraFont:
    class Char:
        def __init__(self, size = 16, ishalf = False):
            self.size = size
            self.ishalf = ishalf
            self.width = size if ishalf else (size + 3) // 4 * 2
            self.data = [[0] * self.width for i in range(size)]
        
        def load_data(self, bs, offset = 0):
            p = offset
            for i in range(self.size):
                for j in range(0, self.width, 2):
                    self.data[i][j+1] = (bs[p] & 0x0F) * 0x11
                    self.data[i][j] = (bs[p] >> 4) * 0x11
                    p += 1
            return p - offset
        
        def to_bytes(self):
            bs = bytearray()
            for row in self.data:
                for j in range(0, self.width, 2):
                    bs.append((row[j+1] >> 4) | (row[j] & 0xF0))
            return bs
    
    def __init__(self, size):
        self.size = size
        self.chars = []
    
    def num(self):
        return len(self.chars)
    
    def load_data(self, bs, offset = 0):
        p = offset
        while p < len(bs):
            ishalf = len(self.chars) >= NUM_HALFWIDTH
            num_bytes = self.size * self.size // 2 if ishalf else self.size * self.size
            if p + num_bytes > len(bs): break
            char = SoraFont.Char(self.size, ishalf)
            p += char.load_data(bs, p)
            self.chars.append(char)
    
    def to_bytes(self):
        bs = bytearray()
        for char in self.chars:
            bs.extend(char.to_bytes())
        return bs
