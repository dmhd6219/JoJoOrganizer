echo off
title jojo timer packer
cls

call clean.cmd

pyinstaller main.py -F -y --clean -i="files\icons\jojo.ico" ^
	--add-data="files\textures;files\textures" ^
	--add-data="files\icons;files\icons" ^
	--add-binary="ffmpeg.exe;." ^
	--add-binary="ffprobe.exe;."

ren dist out

pause