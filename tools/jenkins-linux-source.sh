#!/bin/sh

set -e

virtualenv venv -p python2.7 --system-site-packages
. venv/bin/activate
pip install -r requirements.txt
python tools/execute-specs.py
python tools/build-source-zip.py --revision $1
