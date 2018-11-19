import codecs
import struct, os, sys

from ChList import ChList

CODEC_NAME = 'Sora-SJIS'
DEFAULT_CHLIST_FILENAME = 'chlist.txt'
DIR_PY = os.path.split(os.path.realpath(__file__))[0]

CODEC_SJIS = 'ms932'
CHLIST_ENCODEING = 'utf-8'

class SoraCodec(codecs.Codec):
    def __init__(self, codec_name, chlist_filename, base_codec_name):
        self.codec_name = codec_name
        self.base_codec_name = base_codec_name
        self.ch_map = get_ch_map(chlist_filename, base_codec_name)

    def encode(self, ucs_str, errors='strict'):
        output = bytearray()

        for ch in ucs_str:
            ch = self.ch_map.get(ch, ch)
            output.extend(ch.encode(self.base_codec_name))

        return bytes(output), len(output)

    def decode(self, byte_array, errors='strict'):
        raise UnicodeDecodeError('Decode is not supported.')

def get_ch_map(chlist_filename, base_codec_name):
    ch_map = {}
    chlist = ChList(base_codec_name, chlist_filename, CHLIST_ENCODEING)
    for ch in chlist:
        ch_map[ch.glyph] = ch.code.decode(base_codec_name)
    return ch_map

def get_regentry(codec_name, chlist_filename, base_codec_name):
    sora_codec = SoraCodec(codec_name, chlist_filename, base_codec_name)
    return codecs.CodecInfo(
        name=sora_codec.codec_name,
        encode=sora_codec.encode,
        decode=sora_codec.decode,
    )

def register(codec_name = CODEC_NAME,
             chlist_filename = os.path.join(DIR_PY, DEFAULT_CHLIST_FILENAME),
             base_codec_name = CODEC_SJIS,
             use_sysargs = True):
    if use_sysargs:
        for arg in sys.argv[1:]:
            if arg.startswith('--chlist='):
                chlist_filename = arg[len('--chlist='):]
            elif arg.startswith('--base_encoding='):
                base_codec_name = arg[len('--base_encoding='):]
    codec_name = codec_name.lower()
    base_codec_name = base_codec_name.lower()
    regentry = get_regentry(codec_name, chlist_filename, base_codec_name)
    def search_function(codec_name_search):
        if codec_name_search == codec_name:
            return regentry
        else:
            return None
    codecs.register(search_function)

def get_name():
    return CODEC_NAME
