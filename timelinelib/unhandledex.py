# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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


"""
Code for reporting exceptions that aren't handled anywhere else.
"""


import traceback
from sys import version as python_version
import platform

from timelinelib.version import get_version

import wx


def create_error_message(type, value, tb):
    intro = create_intro_message()
    exception = ("".join(traceback.format_exception(type, value, tb))).strip()
    versions = create_versions_message()
    return "%s\n\n%s\n\n%s" % (intro, exception, versions)


def create_intro_message():
    intro1 = ("An unexpected error has occurred. Please report this by copying "
              "this error message and sending it to "
              "thetimelineproj-user@lists.sourceforge.net.")
    intro2 = ("It would also be useful if you can describe what you did just "
              "before the error occurred.")
    return "%s\n\n%s" % (intro1, intro2)


def create_versions_message():
    return "\n".join([
        "Timeline version: %s" % get_version(),
        "System version: %s" % ", ".join(platform.uname()),
        "Python version: %s" % python_version.replace("\n", ""),
        "wxPython version: %s" % wx.version(),
    ])
