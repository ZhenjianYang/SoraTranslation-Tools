set dir_git=..\..\..
set dir_sora_tr=..\..

set PYTHONPATH=%dir_sora_tr%\SoraTrs

set dir_scripts=%dir_git%\SoraVoiceScripts\cn.fc\py;%dir_git%\SoraVoiceScripts\cn.sc\py;%dir_git%\SoraVoiceScripts\cn.fc\py
set jpfixed=..\[common]\jpfixed.txt
set chlist=chlist.txt

setlocal enabledelayedexpansion
set arg_dirs=
for %%i in ("%dir_scripts:;=" "%") do (
echo %%~i
set "arg_dirs=!arg_dirs! -p %%i"
)

py "%dir_sora_tr%\SoraTrs\MakeChList.py" %arg_dirs% -f "%jpfixed%" %arg_dirs% %chlist%

