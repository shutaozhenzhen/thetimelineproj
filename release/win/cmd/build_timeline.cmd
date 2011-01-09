@echo off
rem This script builds the Timeline installation executable
rem for the Windows target os.

set VERSION=0120

set DIR=C:\Temp\TimelineBuild
set DEL_SUBDIRS=/S
set QUIET_MODE=/Q



rem Start with an empty diretory
echo 1. Preparing the directory.
IF EXIST %DIR% (
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\.hg
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\doc
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\inno
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\bin
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\timeline
    rd %DEL_SUBDIRS% %QUIET_MODE% %DIR%\icalendar
) ELSE (
    mkdir %DIR%
)

rem Checkout the win project
echo 2. Checking out the win project
hg clone http://thetimelineproj.hg.sourceforge.net:8000/hgroot/thetimelineproj/win %DIR% >nul
mkdir %DIR%\bin

rem Checkout timeline
echo 3. Checking out Timeline
mkdir %DIR%\timeline
hg clone http://thetimelineproj.hg.sourceforge.net:8000/hgroot/thetimelineproj/stable %DIR%\timeline >nul

rem Run scons command
echo 4. Running scons command
cd %DIR%\timeline
call scons >nul

rem Adjust timeline.py to work with py2exe
echo 5. Replacing setup.py
copy %DIR%\Inno\timeline.py %DIR%\timeline\timeline.py

rem Adjust paths.py to work with py2exe
echo 6. Replacing paths.py
copy %DIR%\Inno\paths.py %DIR%\timeline\timelinelib\paths.py

rem Include iCalendar
echo 7. Include iCalendar
mkdir %DIR%\timeline\icalendar
copy  %DIR%\icalendar\*.* %DIR%\timeline\icalendar\*.*

rem Update Inno Std script
echo 8. Update Inno Std script

rem Update Inno Exe script
echo 9. Update Inno Exe script

rem Compile Inno Std script
:step10
echo 10. Compile Inno Std script
cd %DIR%\inno
set PATH=%PATH%;"C:\Program Files\Inno Setup 5"
call iscc.exe TimelineStd.iss

rem Setup Std version
:step11
echo 11. Setup Std version
call %DIR%\bin\SetupTimeline%VERSION%Std.exe

rem Wait 60 seconds for Py2Exe to finish it's task
:step12
ping 1.1.1.1 -n 1 -w 60000 >nul

rem Compile Inno Exe script
:step13
echo 13. Compile Inno Exe script
cd %DIR%\inno
set PATH=%PATH%;"C:\Program Files\Inno Setup 5"
call iscc.exe TimelineExeWin7.iss

rem Setup Exe version
:step14
echo 14. Setup Exe version
call %DIR%\bin\SetupTimeline%VERSION%Py2Exe.exe


cd C:\Projekt\Timeline\win\cmd


pause

