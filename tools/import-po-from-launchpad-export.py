#!/usr/bin/env python3
#
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.

"""
Script that imports po files from a tar archive exported from Launchpad.
"""

from subprocess import Popen
import re
import shutil
import os.path
import glob
import tempfile
import sys

from timelinetools.paths import TRANSLATIONS_DIR

if len(sys.argv) != 2:
    print("Usage: python3 import-po-from-launchpad-export.py /path/to/launchpad-export.tar.gz")
    raise SystemExit()

# extract from
archive_path = sys.argv[1]
print(archive_path)

# extract to
tmp_dir = tempfile.mkdtemp()
print(tmp_dir)

# extract
Popen(["tar", "xvvz", "-C", tmp_dir, "--file", archive_path]).wait()

# copy po-files
for pofile in glob.glob(os.path.join(tmp_dir, "timeline", "*.po")):
    dest_name = re.search(r".*-(.*.po)", pofile).group(1)
    dest = os.path.join(os.path.join(TRANSLATIONS_DIR, dest_name))
    shutil.copy(pofile, dest)
    print("Extracted %s" % dest)

# remove tmp dir
shutil.rmtree(tmp_dir)
