@echo off

echo --------------------------------------
echo Revision: %1
echo --------------------------------------


echo --------------------------------------
echo Remove old build and dist directories
echo --------------------------------------
rmdir /S /Q build >> nul
rmdir /S /Q dist >> nul
del /S /Q inno\out >> nul

echo --------------------------------------
echo Create translations
echo --------------------------------------
pushd ..
python generate-mo-files.py
popd

echo --------------------------------------
echo Building distribution
echo --------------------------------------
pyinstaller timeline.spec

echo --------------------------------------
echo Package distribution
echo --------------------------------------
python mod_iss_timeline_version.py . %1
pushd inno
iscc.exe timeline2Win32.iss
popd