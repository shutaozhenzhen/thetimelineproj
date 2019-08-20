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


USAGE = """
    Usage:
        python mod_iss_timeline_version.py   project-tools-dir
"""


def get_version(versionfile):
    with open(versionfile, "r") as f:
        text = f.read()
        lines = text.split("\n")
        for line in lines:
            if line[0:7] == "VERSION":
                break
    line = line.split("(", 1)[1]
    line = line.split(")", 1)[0]
    major, minor, bug = line. split(", ")
    app_ver_name = "Timeline %s.%s.%s" % (major, minor, bug)
    output_base_filename = "SetupTimeline%s%s%sWin32" % (major, minor, bug)
    print("[INFO] Version found: %s" % app_ver_name)
    print("[INFO] Filename: %s" % output_base_filename)
    return app_ver_name, output_base_filename


def modify_iss_file(target, app_ver_name, output_base_filename):
    with open(target, "r") as f:
        text = f.read()
    with open(target, "w") as f:
        lines = text.split("\n")
        for line in lines:
            if line[0:11] == "AppVerName=":
                line = "AppVerName=%s" % app_ver_name
                f.write(line + "\n")
                print("[INFO] Iss file version line: %s" % line)
            elif line[0:19] == "OutputBaseFilename=":
                line = "OutputBaseFilename=%s" % output_base_filename
                f.write(line + "\n")
                print("[INFO] Iss base filename line: %s" % line)
            else:
                f.write(line + "\n")


def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "inno", "timeline2Win32.iss")
    version = os.path.join(project_dir, "..", "..", "source", "timelinelib", "meta", "version.py")
    print("Script: mod2_timeline_iss_win32.py")
    print("Target:", target)
    print("Version:", version)
    if not os.path.exists(target):
        print("[ERROR] Can't find target file: %s" % target)
        return
    if not os.path.exists(version):
        print("[ERROR] Can't find version file: %s" % version)
        return
    app_ver_name, output_base_filename = get_version(version)
    modify_iss_file(target, app_ver_name, output_base_filename)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE)
    else:
        if not os.path.exists(sys.argv[1]):
            print(USAGE)
            print("[ERROR] Can't find project root dir: %s" % sys.argv[1])
        else:
            main()
