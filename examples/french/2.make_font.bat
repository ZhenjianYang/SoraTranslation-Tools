set dir_git=..\..\..
set dir_sora_tr=..\..

set PYTHONPATH=%dir_sora_tr%\SoraTrs

set range_all=20-FFFF
set range_noascii=A0-FFFF

set range=%range_noascii%

set dir_old_fonts=fonts_old
set dir_fonts=fonts
set font=font.ttf
set fontwidth=FONTWDTH._DA
set chlist=chlist.txt

if /I "%range%"=="%range_all%" set "arg_fontwidth=-w "%fontwidth%""

del /F /Q "%dir_fonts%\%fontwidth%"
py "%dir_sora_tr%\SoraTrs\MakeFont.py" -x 2 -y 2 -s 48 -b 1.00 -f "%font%" -c "%chlist%" -p "%dir_old_fonts%" -r %range% %arg_fontwidth% "%dir_fonts%"
