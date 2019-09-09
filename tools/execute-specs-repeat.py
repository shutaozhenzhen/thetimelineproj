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


import os
import os.path
import subprocess
import sys


TIMES_TO_REPEAT = 100
GDB_PREFIX = ["gdb", "-ex='set confirm on'", "-ex=r", "-ex=quit", "--args"]


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "execute-specs.py")
    cmd = [sys.executable, path] + sys.argv[1:]
    if os.environ.get("GDB") == "on":
        cmd = GDB_PREFIX + cmd
    print("Running %s x %d" % (cmd, TIMES_TO_REPEAT))
    sys.stdout.flush()
    for i in range(TIMES_TO_REPEAT):
        print("Try %d" % (i+1))
        sys.stdout.flush()
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            sys.exit(1)
