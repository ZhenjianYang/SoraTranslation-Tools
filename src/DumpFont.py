import sys, os
import png
from SoraFont import SoraFont

NUM_ONE_ROW = 32
def SaveToPng(ppng, font, grid = False):
    num_rows = (font.num() + NUM_ONE_ROW - 1) // NUM_ONE_ROW
    width = font.size * NUM_ONE_ROW
    height = font.size * num_rows

    palette = [(0xFF, 0, 0, i) for i in range(256)]

    rows = [[0] * width for i in range(height)]

    r0, c0 = 0, 0
    for ch in font.chars:
        for r in range(ch.size):
            if r0 + r >= height:
                break
            for c in range(ch.width):
                if c0 + c >= width:
                    break
                rows[r0+r][c0+c] = ch.data[r][c]
        c0 += font.size
        if c0 >= width:
            r0, c0 = r0 + font.size, 0
    
    if grid:
        for i in range(0, height, font.size):
            rows[i] = [0xFF] * width
        for j in range(0, width, font.size):
            for i in range(height):
                rows[i][j] = 0xFF
    
    fs = open(ppng, 'wb')
    pw = png.Writer(width, height, palette=palette)
    pw.write(fs, rows)
    fs.close()

def getSubFiles(dir, ext = '.dat'):
    ret = []
    dir_list =  os.listdir(dir)
    for file in dir_list:
        path = os.path.join(dir, file)
        if os.path.splitext(file)[1].lower() == ext and os.path.isfile(path):
            ret.append(file)
    return ret

def main():
    grid = False
    istart = 1
    if len(sys.argv) > 1 and sys.argv[1][0] == '-':
        istart += 1
        for c in sys.argv[1][1:]:
            if c == 'g':
                grid = True

    if len(sys.argv) < istart + 1 :
        print('%s [-{modes}] font_dir [out_dir]' % sys.argv[0])
        print('  modes list:')
        print('    g: add grid')
        print('    default : output png(no grids)')
        return
    
    font_dir, istart = sys.argv[istart], istart + 1
    out_dir = font_dir if len(sys.argv) <= istart else sys.argv[istart]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    files = getSubFiles(font_dir)
    for file in files:
        fn = os.path.splitext(file)[0].rstrip(' ')
        if fn.lower().startswith('font'):
            size = fn[4:]
            try: size = int(size)
            except: continue
            font = None
            with open(os.path.join(font_dir, file), 'rb') as fs:
                bs = fs.read()
                font = SoraFont(size)
                font.load_data(bs)
            if font:
                print('Saving {0}...'.format(file + ".png"))
                SaveToPng(os.path.join(out_dir, file + ".png"), font, grid)

if __name__ == '__main__':
    main()
