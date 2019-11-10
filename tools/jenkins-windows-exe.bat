python tools/execute-specs.py --write-testlist testlist.txt
cd tools\winbuildtools
set path=c:\pgm\python37;c:\pgm\python37\Scripts;%PATH%
buildwinsetup.cmd %1
