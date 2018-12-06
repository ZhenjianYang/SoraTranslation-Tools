set dir_git=..\..\..
set dir_sora_tr=..\..

set PYTHONPATH=%dir_sora_tr%\SoraTrs

set dir_fonts=fonts_old
set dir_png=fonts_old_png

py "%dir_sora_tr%\SoraTrs\DumpFont.py" -g %dir_fonts% %dir_png%