set dir_git=..\..\..
set dir_sora_tr=..\..

set PYTHONPATH=%dir_sora_tr%\SoraTrs

set half=half.txt
set jpfixed=..\[common]\jpfixed.txt
set chlist=chlist.txt

py "%dir_sora_tr%\SoraTrs\MakeChList.py" -f "%jpfixed%" -h %half% %chlist%

