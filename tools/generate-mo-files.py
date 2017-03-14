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


from os.path import join, exists
import os
import subprocess

from timelinetools.paths import TRANSLATIONS_DIR


def generate_mo_files():
    for file in os.listdir(TRANSLATIONS_DIR):
        if file.endswith(".po"):
            generate_mo_file(TRANSLATIONS_DIR, file[:-3])


def generate_mo_file(po_directory, po_name):
    ensure_directory_exists(mo_destination(po_directory, po_name))
    subprocess.check_call(build_msgfmt_command(po_directory, po_name))


def build_msgfmt_command(po_directory, po_name):
    command = []
    command.append("msgfmt")
    command.append("-o")
    command.append(join(mo_destination(po_directory, po_name), "timeline.mo"))
    command.append(join(po_directory, "%s.po" % po_name))
    return command


def mo_destination(po_directory, po_name):
    return join(po_directory, po_name, "LC_MESSAGES")


def ensure_directory_exists(directory):
    if not exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    generate_mo_files()
