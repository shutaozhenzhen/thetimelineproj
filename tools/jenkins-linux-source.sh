#!/bin/sh

set -e

virtualenv venv -p python2.7 --system-site-packages
. venv/bin/activate
pip install git+https://github.com/thetimelineproj/humblewx.git
python tools/build-source-zip.py --revision $1
