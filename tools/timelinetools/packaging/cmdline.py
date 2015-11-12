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


import os
import sys


def warn_if_file_exists(zip_file_name):
    if os.path.exists(zip_file_name):
        continue_despite_warning("File '%s' already exists." % zip_file_name)


def continue_despite_warning(warning_text):
    while True:
        answer = raw_input("%s Continue anyway? [y/N] " % warning_text)
        if answer == "n" or answer == "":
            sys.exit(1)
        elif answer == "y":
            return
