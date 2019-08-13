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


from os.path import join, relpath
import argparse
import os
import subprocess

from timelinetools.paths import ROOT_DIR
from timelinetools.paths import SOURCE_DIR
from timelinetools.paths import TRANSLATIONS_DIR


def generate_pot_file():
    subprocess.check_call(build_xgettext_command(parse_arguments()), cwd=ROOT_DIR)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outfile", default=relpath(join(TRANSLATIONS_DIR, "timeline.pot"), ROOT_DIR))
    return parser.parse_args()


def build_xgettext_command(arguments):
    command = []
    command.append("xgettext")
    command.append("-o")
    command.append(arguments.outfile)
    command.append("--add-comments=TRANSLATORS")
    command.extend(sorted(find_py_files_in(SOURCE_DIR)))
    return command


def find_py_files_in(directory):
    py_files = []
    for (root, dirs, files) in os.walk(directory):
        py_files += [relpath(join(root, f), ROOT_DIR) for f in files if f.endswith(".py")]
    return py_files


if __name__ == "__main__":
    generate_pot_file()
