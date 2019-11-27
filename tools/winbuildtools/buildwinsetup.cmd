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
xcopy /S ..\..\icons\*.*  .\dist\icons\*.*
xcopy /S ..\..\translations\ca\*.*  .\dist\translations\ca\*.*
xcopy /S ..\..\translations\de\*.*  .\dist\translations\de\*.*
xcopy /S ..\..\translations\el\*.*  .\dist\translations\el\*.*
xcopy /S ..\..\translations\es\*.*  .\dist\translations\es\*.*
xcopy /S ..\..\translations\eu\*.*  .\dist\translations\eu\*.*
xcopy /S ..\..\translations\fr\*.*  .\dist\translations\fr\*.*
xcopy /S ..\..\translations\gl\*.*  .\dist\translations\gl\*.*
xcopy /S ..\..\translations\he\*.*  .\dist\translations\he\*.*
xcopy /S ..\..\translations\it\*.*  .\dist\translations\it\*.*
xcopy /S ..\..\translations\ko\*.*  .\dist\translations\ko\*.*
xcopy /S ..\..\translations\lt\*.*  .\dist\translations\lt\*.*
xcopy /S ..\..\translations\nl\*.*  .\dist\translations\nl\*.*
xcopy /S ..\..\translations\pl\*.*  .\dist\translations\pl\*.*
xcopy /S ..\..\translations\pt\*.*  .\dist\translations\pt\*.*
xcopy /S ..\..\translations\pt_BR\*.*  .\dist\translations\pt_BR\*.*
xcopy /S ..\..\translations\ru\*.*  .\dist\translations\ru\*.*
xcopy /S ..\..\translations\sv\*.*  .\dist\translations\sv\*.*
xcopy /S ..\..\translations\tr\*.*  .\dist\translations\tr\*.*
xcopy /S ..\..\translations\vi\*.*  .\dist\translations\vi\*.*
xcopy /S ..\..\translations\zh_CH\*.*  .\dist\translations\zh_CH\*.*


echo --------------------------------------
echo Create distributable
echo --------------------------------------
pushd inno
iscc.exe timeline2Win32.iss
popd
