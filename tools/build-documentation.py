#!/usr/bin/env python
#
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


import argparse
import os

from timelinetools.crossplatform import is_windows
from timelinetools.paths import DOCUMENTATION_DIR
from timelinetools.run import run_cmd_and_exit_if_fails


def main():
    build_documentation(parse_arguments())


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="html")
    parser.add_argument("--clean", action="store_true")
    return parser.parse_args()


def build_documentation(arguments):
    if arguments.clean:
        make("clean")
    make(arguments.target)


def make(target):
    run_cmd_and_exit_if_fails(get_make_program() + [target], cwd=DOCUMENTATION_DIR)


def get_make_program():
    if is_windows():
        return [os.path.join(DOCUMENTATION_DIR, "make.bat")]
    else:
        return ["make"]


if __name__ == '__main__':
    main()
