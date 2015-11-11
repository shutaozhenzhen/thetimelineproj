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


TYPE_DEV = "development"
TYPE_BETA = "beta"
TYPE_FINAL = ""

VERSION = (1, 9, 0)
TYPE = TYPE_DEV


def get_version():
    return get_readme_version()


def get_readme_version():
    string = get_version_number_string()
    if TYPE:
        string += " %s" % TYPE
    return string


def get_version_number_string():
    return "%s.%s.%s" % VERSION


def is_dev():
    return TYPE == TYPE_DEV
