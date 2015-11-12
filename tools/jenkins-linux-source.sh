#!/bin/sh

set -e

virtualenv venv -p python2.7 --system-site-packages
. venv/bin/activate
pip install -r requirements.txt
python test/execute-specs-repeat.py
python tools/package-source.py --revision $1
