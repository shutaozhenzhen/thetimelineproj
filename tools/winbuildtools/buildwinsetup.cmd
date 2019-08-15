@echo off

echo --------------------------------------
echo Remove old build and dist directories
echo --------------------------------------
rmdir /S /Q build >> nul
rmdir /S /Q dist >> nul
del /S /Q inno\out >> nul

echo --------------------------------------
echo Building distribution
echo --------------------------------------
pyinstaller timeline.spec

echo --------------------------------------
echo Package distribution
echo --------------------------------------
pushd inno
iscc.exe timeline2Win32.iss
popd

pause