echo off
title jojo timer packer
cls

call clean.cmd

set PYTHONOPTIMIZE=1
pyinstaller main.py -w -F --clean -y -i="files\icons\jojo.ico" ^
	--add-data="files\textures;files\textures" ^
	--add-data="files\icons;files\icons" ^
	--add-binary="ffmpeg.exe;." ^
	--add-binary="ffprobe.exe;."

ren dist out

pause