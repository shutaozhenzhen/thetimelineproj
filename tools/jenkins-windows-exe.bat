set path=c:\pgm\python37;c:\pgm\python37\Scripts;%PATH%
virtualenv venv -p python3 --system-site-packages
. venv/bin/activate
pip install git+https://github.com/thetimelineproj/humblewx.git
pip install icalendar
pip install Markdown
pip install pysvg-py3
pip install Pillow
python tools/execute-specs.py --write-testlist testlist.txt
cd tools\winbuildtools
buildwinsetup.cmd %1
