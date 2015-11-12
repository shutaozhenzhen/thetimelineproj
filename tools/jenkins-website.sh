#!/bin/sh

set -e

USERNAME="rickardlindberg"
HOST="$USERNAME,thetimelineproj@web.sourceforge.net"
ROOT=/home/project-web/thetimelineproj
RSYNC_FLAGS="--recursive --del --progress"

cd documentation
make clean html
rsync $RSYNC_FLAGS _build/html/ $HOST:$ROOT/htdocs
curl -X POST http://readthedocs.org/build/thetimelineproj
