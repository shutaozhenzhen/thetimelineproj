#!/bin/sh

set -e

virtualenv venv -p python3 --system-site-packages
. venv/bin/activate
pip install git+https://github.com/thetimelineproj/humblewx.git
pip install icalendar
pip install Markdown
pip install pysvg-py3
pip install Pillow
python tools/execute-specs-repeat.py --write-testlist testlist.txt
python tools/build-source-zip.py --revision $1
