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


import sys
import os


FILE = "timeline.py"


def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "source", "timeline.py")
    print "Script: mod2_timeline_py.py"
    print "Target:", target
    
    f = open(target, "r")
    text = f.read()
    f.close()
    f = open(target, "w")
    lines = text.split("\n")
    for line in lines:
        if line[0:16] == "sys.path.insert(":
            f.write("exepath = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))\n")
            f.write("sys.path.insert(0, exepath)\n")
        else:
            f.write(line + "\n")
    f.close()


if __name__ == "__main__":
    main()
