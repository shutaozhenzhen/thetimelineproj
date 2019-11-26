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
echo Modify paths.py
echo --------------------------------------
python mod_paths.py .

echo --------------------------------------
echo Modify version file and iss file
echo --------------------------------------
python mod_iss_timeline_version.py . %1

echo --------------------------------------
echo Building distribution
echo --------------------------------------
pyinstaller timeline.spec

echo --------------------------------------
echo Copying icons and translations to dist
echo --------------------------------------
mkdir .\dist\icons\event_icons
mkdir .\dist\translations
xcopy ..\..\icons\*.*  .\dist\icons\*.*
xcopy ..\..\icons\event_icons\*.*  .\dist\icons\event_icons\*.*
xcopy ..\..\translations  .\dist\translations

echo --------------------------------------
echo Create distributable
echo --------------------------------------
pushd inno
iscc.exe timeline2Win32.iss
popd
