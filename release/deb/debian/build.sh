#!/bin/sh

# Change to parent directory of this file
cd `dirname $0`
cd ..

patch -p0 < debian/pathfix.patch
su --command "dpkg-buildpackage -B -tc"
patch -p0 -R < debian/pathfix.patch
