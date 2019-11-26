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


def main():
    project_dir = sys.argv[1]
    path = os.path.join(project_dir, "..", "..", "source", "timelinelib", "config", "paths.py")
    text = None
    with open(path) as f:
        text = f.read()
    collector = []
    for line in text.split('\n'):
        if line.strip().startswith("_ROOT ="):
            line = "_ROOT = '.'"
        collector.append(line.strip())
    text = '\n'.join(collector)
    with open(path, "w") as f:
        f.write(text)
    print("paths.py modified")
    print(text)


main()
