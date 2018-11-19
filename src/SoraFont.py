import struct

NUM_HALFWIDTH = 16 * 12

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
