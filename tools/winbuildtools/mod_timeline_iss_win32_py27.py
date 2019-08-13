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


def get_version(versionfile):
    f = open(versionfile, "r")
    text = f.read()
    lines = text.split("\n")
    for line in lines:
        if line[0:7] == "VERSION":
            break
    f.close()
    #VERSION = (0, 14, 0)
    line = line.split("(", 1)[1]
    line = line.split(")", 1)[0]
    major, minor, bug = line. split(", ")
    app_ver_name = "Timeline %s.%s.%s" % (major, minor, bug)
    output_base_filename = "SetupTimeline%s%s%sPy2ExeWin32" % (major, minor, bug)
    return (app_ver_name, output_base_filename)

def modify_iss_file(target, app_ver_name, output_base_filename):
    f = open(target, "r")
    text = f.read()
    f.close()
    f = open(target, "w")
    lines = text.split("\n")
    for line in lines:
        if line[0:11] == "AppVerName=":
            f.write("AppVerName=%s\n" % app_ver_name)
        elif line[0:19] == "OutputBaseFilename=":
            f.write("OutputBaseFilename=%s\n" % output_base_filename)
        else:
            f.write(line + "\n")

def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "tools", "winbuildtools", "inno", "timelineWin32Py27.iss")
    version = os.path.join(project_dir, "source", "timelinelib", "meta", "version.py")
    print("Script: mod_timeline_iss_win32_py27.py")
    print("Target:", target)
    print("Version:", version)

    app_ver_name, output_base_filename = get_version(version)
    modify_iss_file(target, app_ver_name, output_base_filename)


if __name__ == "__main__":
    main()
