# SoraTranslation-Tools

The *Trails in the Sky* series (Steam) uses code page 932. So Japanese (and English, since ASCII is a subset of cp932) characters are natively supported while other languages (Chinese, French, Korean, etc.) containing characters not included in cp932 are not.

This project tries to add the support for these characters.   

#### Required libs:   
```
pip install pypng freetype-py
```

## How to   
**3 Steps:**   
1. [Create chlist.txt](README.md#1-Create-chlisttxt) 
2. [Encode strings with SoraSJIS.py](README.md#2-Encode-strings-with-SoraSJISpy)   
3. [Create fonts files](README.md#3-Create-fonts-files)  

Here are some examples:  [examples/chinese](examples/chinese), [examples/french](examples/french) 

### 1. Create chlist.txt   

The basic idea of this project is replacing some Japanese characters with characters which are not included in cp932. So we need a replacement table. We use chlist.txt to define this table.

chiist.txt is a text file, its encoding is utf8 (No BOM), and the format of each line is:   
```
<SJIS Code>=<ucs code/ucs character>
```
For example:   
```
B1=à
88A8=们
```
means we replace 'ｱ'(sjis:B1) with 'à', and replace '葵'(sjis:88A8) with '们'.

We should create a chlist.txt containing all characters we need but not belong to cp932. chlist.txt can be manually created, or   

#### Use [MakeChList.py](SoraTrs/MakeChList.py) to create chlist.txt   
[MakeChList.py](SoraTrs/MakeChList.py) is a tool which can help us create chlist.txt.

Usage:    
`MakeChList.py [-f fixed_list] [-h halfwidth_characters_list] [-f fullwidth_characters_list] chlist.txt` 

We divide the range of cp932 into 3 parts:   

- **ASCII part (20-7F)**, all characters in this part will not be replaced.   
- **halfwidth-kana part (A0-DF)**, characters in this part will be replaced by characters in file *halfwidth_characters_list*. Please note that the width of characters in this part is half of fullwidth characters.  
- **fullwidth part (8140-9FFC, E040-EFFC)**, characters in this part will be replaced by characters in file *fullwidth_characters_list*.   

We can assign a *fixed_list*, characters listed in *fixed_list* also won't be replaced.   

### 2. Encode strings with [SoraSJIS.py](SoraTrs/SoraSJIS.py)   
With the replacement table chlist.txt, we defined a code page, we need to encode strings with this code page. [SoraSJIS.py](SoraTrs/SoraSJIS.py) is such a code page defined by chlist.txt and can be used just as other standard code pages.

Here is an example:
```python
import SoraSJIS

SoraSJIS.register(chlist=r'D:\chlist.txt')
code_name = SoraSJIS.get_name()
string = 'à们a谷'
bs = string.encode(code_name)
print(bs)
```
If the contents of D:\chlist.txt are:
```
B1=à
88A8=们
```
The result of these code is:
```
b'\xB1\x88\xA8\x61\x92\x4A'
```
Please note that characters not contained in chlist.txt will be encoded with cp932.

The path of chlist.txt can be assigned with command arguments.   
For example, we change the code to:   
```python
import SoraSJIS

SoraSJIS.register()
code_name = SoraSJIS.get_name()
string = 'à们a谷'
bs = string.encode(code_name)
print(bs)
```
And run it with:
```
py xxxx.py --chlist=D:\chlist.txt
```
We will get the same result.

### 3. Create fonts files

Since chlist.txt is a replacement table, we just replace glyphs listed in chlist.txt.So we need to extract all FONT*.DAT files from ED6_DT00/ED6_DT20 with [falcncvt tool](http://www.pokanchan.jp/dokuwiki/software/falcnvrt/start) first. 

And we use [MakeFont.py](SoraTrs/MakeFont.py) to create:   
```
MakeFont.py [-b bold] [-x dx] [-y dy] [-s fontsize] [-r range] -f ttf_file -c chlist.txt -p dir_fonts outputfolder
```
 - -b : embolden, e.g. '-b 0.75' means 'embolden 0.75 pixel'
 - -x : move rightwards, e.g. '-x -2.5' means 'move leftwards 2.5 pixels'
 - -y : move upwards, e.g. '-x 1.5' means 'move upwards 1.5 pixels'
 - -s : set the font size, e.g. '-s 48' means 'set font size to 48'   
Since the game contains different sizes of fonts, MakeFont.py will create them together. These 4 arguments are base on size 64. Arguments for other sizes will be calculated proportionately. e.g. above examples for size 128 means 'embolden 1.5 pixel', 'move leftwards 5 pixels', 'move upwards 3 pixels', 'set font size to 96'.   
- -r : sjis range, only these characters in this range will be replaced. e.g. '-r A0-FFFF'.
- -f : assign the path of ttf file.
- -c : assign the path of chlist.txt.
- -p : assign the path of the folder containing extracted FONT*.DAT files。
- outputfolder ： the output folder.

### The last

The last step is importing modified files back to the game. You may try [ed6back](https://github.com/Ouroboros/JuusanKoubou/tree/master/Source/Falcom/ED6Back). Or if you are using the latest [SoraVoice](https://github.com/ZhenjianYang/SoraVoice), you can just copy all fonts files to `voice/fonts`, and copy all scripts files to `voice/scena`.

And please check these examples:  [examples/chinese](examples/chinese), [examples/french](examples/french). You may find more details about these tools.
