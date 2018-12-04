set dir_git=..\..\..
set dir_sora_tr=..\..

set PYTHONPATH=%dir_git%\EDDecompiler\Decompiler;%dir_git%\PyLibs;%dir_sora_tr%\SoraTrs

set chlist=chlist.txt
set sorasjis=%dir_sora_tr%\SoraTrs\SoraSJIS.py
set dir_game=dir

set dir_py=py
set dir_scena=scena

mkdir %dir_scena%

for %%i in ("%dir_py%\*.py") do (
title Compiling %%~ni
py "%%i" "--cppy=%sorasjis%" "--chlist=%chlist%" "--gp=%dir_game%" "%dir_scena%"
)


