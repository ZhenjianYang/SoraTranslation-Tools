
CHLIST_ENCODEING = 'utf-8'
BASE_CODEC = 'ms932'
CHLIST_ENCODEING = 'utf-8'

class Char:
    def __init__(self, code, glyph):
        self.code = code
        self.glyph = glyph
    def __lt__(self, other):
        if len(self.code) != len(other.code):
            return len(self.code) < len(other.code)
        else:
            return self.code < other.code

class ChList:
    def __init__(self, base_codec = BASE_CODEC, chlist_filename = None, chlist_encoding = CHLIST_ENCODEING):
        self.base_codec = base_codec
        if chlist_filename:
            self.open(chlist_filename, chlist_encoding)
        else:
            self.ch_list, self.ch_map = [], {}

    def open(self, chlist_filename, chlist_encoding = CHLIST_ENCODEING):
        ch_map = {}
        with open(chlist_filename, mode='r', encoding=chlist_encoding) as file:
            for line in file:
                line = list(line)
                while line and line[-1] in '\r\n\t': line.pop()
                line = ''.join(line)
                if not line: continue
                i = line.find('=', 1)
                if i < 0:
                    code, glyph = line, None
                else:
                    code, glyph = line[:i], line[i+1:]

                if len(code) == 1:
                    code = code.encode(self.base_codec)
                else:
                    code = bytes.fromhex(code)
                    test = code.decode(self.base_codec)
                    if len(test) != 1:
                        raise UnicodeDecodeError('Decode Error:' + str(code))
                if not glyph:
                    glyph = code.decode(self.base_codec)
                elif len(glyph) > 1:
                    glyph = chr(int(glyph, 16))
                
                ch_map[code] = Char(code, glyph)
        
        self.ch_map = ch_map
        self.ch_list = sorted(ch_map.values())
    
    def find(self, code):
        return self.ch_map.get(code, None)

    def all_chars(self):
        return self.ch_list
    
    def __iter__(self):
        return iter(self.ch_list)

