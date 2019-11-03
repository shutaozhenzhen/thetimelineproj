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
import subprocess


USAGE = """
    Usage:
        python mod_iss_timeline_version.py   project-tools-dir   revision
"""


def get_hash(revision):
    try:
        return subprocess.check_output([
            "hg", "id",
            "-r", revision,
        ]).decode("utf-8").strip().split(" ")[0]
    except subprocess.CalledProcessError as e:
        print("ERROR:", str(e))
        raise


def get_revision_date(revision):
    try:
        return subprocess.check_output([
            "hg", "log",
            "-r", revision,
            "--template", "{date|shortdate}",
        ]).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print("ERROR:", str(e))
        raise


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
    revision = sys.argv[2]
    print("Revision:", revision)
    hash_value = get_hash(sys.argv[2])
    revision_date = get_revision_date(sys.argv[2])
    if revision == 'tip':
        output_base_filename = "timeline-%s.%s.%s-beta-%s-%s-Win32Setup" % (major, minor, bug, hash_value, revision_date)
    else:
        output_base_filename = "timeline-%s.%s.%s-Win32Setup" % (major, minor, bug)
        with open(versionfile, "r") as f:
            text = f.read()
        text = text.replace('TYPE = TYPE_DEV', 'TYPE = TYPE_FINAL')
        text = text.replace('REVISION_DATE = ""', f'REVISION_HASH = "{revision_date}"')
        text = text.replace('REVISION_DATE = ""', f'REVISION_HASH = "{revision_date}"')
        with open(versionfile, "w") as f:
            f.write(text)
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
    versionfile_path = os.path.join(project_dir, "..", "..", "source", "timelinelib", "meta", "version.py")
    print("Script: mod2_timeline_iss_win32.py")
    print("Target:", target)
    print("Version:", versionfile_path)
    if not os.path.exists(target):
        print("[ERROR] Can't find target file: %s" % target)
        return
    if not os.path.exists(versionfile_path):
        print("[ERROR] Can't find version file: %s" % versionfile_path)
        return
    app_ver_name, output_base_filename = get_version(versionfile_path)
    modify_iss_file(target, app_ver_name, output_base_filename)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
    else:
        if not os.path.exists(sys.argv[1]):
            print(USAGE)
            print("[ERROR] Can't find project root dir: %s" % sys.argv[1])
        else:
            main()
