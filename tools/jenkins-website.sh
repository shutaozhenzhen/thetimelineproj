#!/bin/sh

set -e

USERNAME="rickardlindberg"
HOST="$USERNAME,thetimelineproj@web.sourceforge.net"
ROOT=/home/project-web/thetimelineproj
RSYNC_FLAGS="--recursive --del --progress"

python3 tools/build-documentation.py --clean
rsync $RSYNC_FLAGS documentation/_build/html/ $HOST:$ROOT/htdocs
curl -X POST http://readthedocs.org/build/thetimelineproj
