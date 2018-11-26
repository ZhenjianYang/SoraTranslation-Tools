import sys, os

from CodeTable import CodeTable

FILE_ENCODING = 'utf-8'
BASE_CODEC = 'ms932'

def PrintUsage():
    print('%s [-f fixed_chlist] [-h halfwidth_chars] [-t fullwidth_chars] [-p pyfiles] [-c inputfile encoding] [-x] out_chlist' % sys.argv[0])
    print('    -f     : a file, fixed chlist')
    print('    -h     : txt file or folder, halfwidth chars')
    print('    -t     : txt file or folder, fullwidth chars')
    print('    -p     : py file or folder, fullwidth chars')
    print('    -c     : inputfile encoding, default: ms932')
    print('    -x     : Creat fixed chlist')
    print('    -h, -t, -p can appear more than one times')

def GetFiles(dir, ext = '.txt'):
    ext = ext.lower()
    if os.path.isdir(dir):
        ret = []
        dir_list =  os.listdir(dir)
        for file in dir_list:
            path = os.path.join(dir, file)
            if os.path.splitext(file)[1].lower() == ext and os.path.isfile(path):
                ret.append(path)
    else:
        ret = [dir]
    return ret

def GetParams():
    fn_fch = ''
    fns_txt_hw = []
    fns_txt_fw = []
    fns_py = []
    fn_ch_out = ''
    codec_in = FILE_ENCODING
    gen_fixed = False
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] and sys.argv[i][0] == '-' and i + 1 < len(sys.argv):
            if i + 1 >= len(sys.argv):
                print('Bad parameter: {0}'.format(sys.argv[i]))
                i += 1
            elif sys.argv[i][1:] == 'f':
                fn_fch = sys.argv[i+1]
                i += 2
            elif sys.argv[i][1:] == 'h':
                fns_txt_hw.extend(GetFiles(sys.argv[i+1], '.txt'))
                i += 2
            elif sys.argv[i][1:] == 't':
                fns_txt_fw.extend(GetFiles(sys.argv[i+1], '.txt'))
                i += 2
            elif sys.argv[i][1:] == 'p':
                fns_py.extend(GetFiles(sys.argv[i+1], '.py'))
                i += 2
            elif sys.argv[i][1:] == 'c':
                codec_in = sys.argv[i+1]
                i += 2
            elif sys.argv[i][1:] == 'x':
                gen_fixed = True
                i += 1
            else:
                print('Bad parameter: {0}'.format(sys.argv[i]))
                i += 1
        else:
            fn_ch_out = sys.argv[i]
            i += 1
    return None if not fn_ch_out else fn_fch, fns_txt_hw, fns_txt_fw, fns_py, codec_in, gen_fixed, fn_ch_out

def GetChars(filename, codec_in = BASE_CODEC, ispy=False):
    ret = set()
    with open(filename, mode='r', encoding=codec_in) as file:
        for line in file:
            if ispy:
                t = []
                i = 0
                while i < len(line):
                    if line[i] == '"':
                        j = line.find('"', i+1)
                        if j >= 0:
                            t.append(line[i+1:j])
                            i = j + 1
                        else: break
                    elif line[i] == "'":
                        j = line.find("'", i+1)
                        if j >= 0:
                            t.append(line[i+1:j])
                            i = j + 1
                        else: break
                    else:
                        i += 1
                line = ''.join(t)
            for ch in line:
                if  ord(ch) >= 0x20 and ord(ch) != 0xFEFF:
                    ret.add(ch)
    return sorted(ret)

def main():
    params = GetParams()
    if not params:
        PrintUsage()
        return
    fn_fch, fns_txt_hw, fns_txt_fw, fns_py, codec_in, gen_fixed, fn_ch_out = params

    ct = CodeTable()
    ct.add_fixed(fn_fch)

    hws, fws = [], []
    for txt in fns_txt_hw:
        print('Collecting chars from {0}...'.format(txt))
        hws.extend(GetChars(txt, codec_in))
    for txt in fns_txt_fw:
        print('Collecting chars from {0}...'.format(txt))
        fws.extend(GetChars(txt, codec_in))
    for py in fns_py:
        print('Collecting chars from {0}...'.format(py))
        fws.extend(GetChars(py, codec_in, ispy=True))
    
    hws, fws = sorted(set(hws)), sorted(set(fws))
    if gen_fixed:
        for ch in hws + fws:
            try: bs = ch.encode(BASE_CODEC)
            except:
                print('Not a sjis char: ' + ch)
                continue
            sjis = 0
            for b in bs: sjis = (sjis << 8) | b
            ct.add_fixed_sjis(sjis, ch)
        chars = ct.get_fixed_list() 
    else:
        for ch in hws:
            ct.add(ch, half=True)
        for ch in fws:
            ct.add(ch)
        chars = ct.get_added_list() 
    with open(fn_ch_out, encoding=FILE_ENCODING, mode='w') as file:
        for sjis, ucs in chars:
            file.write('{0:X}={1}\n'.format(sjis, chr(ucs)))

if __name__ == '__main__':
    main()
