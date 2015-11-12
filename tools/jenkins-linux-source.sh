#!/bin/sh

set -e

virtualenv venv -p python2.7 --system-site-packages
. venv/bin/activate
pip install -r requirements.txt
python tools/sanity-check.py
python tools/package-source.py --revision $1
