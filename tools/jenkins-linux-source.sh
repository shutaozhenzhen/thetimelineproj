#!/bin/sh

set -e

virtualenv venv -p python3 --system-site-packages
. venv/bin/activate
pip install git+https://github.com/thetimelineproj/humblewx.git
python tools/build-source-zip.py --revision $1
