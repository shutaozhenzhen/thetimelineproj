#!/usr/bin/env python
#
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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


from os.path import dirname, join, normpath
import os
import subprocess


def generate_pot_file():
    repo_root = normpath(join(dirname(__file__), ".."))
    subprocess.check_call(build_xgettext_command(repo_root))


def build_xgettext_command(repo_root):
    command = []
    command.append("xgettext")
    command.append("-o")
    command.append(join(repo_root, "translations", "timeline.pot"))
    command.append("--add-comments=TRANSLATORS")
    command.extend(find_py_files_in(join(repo_root, "source")))
    return command


def find_py_files_in(directory):
    py_files = []
    for (root, dirs, files) in os.walk(directory):
        py_files += [join(root, f) for f in files if f.endswith(".py")]
    return py_files


if __name__ == "__main__":
    generate_pot_file()
