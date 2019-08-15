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

"""
This is the module used to start Timeline.
"""


import gettext
import locale
import os
import platform
import sys

# Make sure that we can import timelinelib
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

# from timelinelib.config.paths import LOCALE_DIR
# from timelinelib.meta.about import APPLICATION_NAME


if platform.system() == "Windows":
    # The appropriate environment variables are set on other systems
    language, encoding = locale.getdefaultlocale()
    os.environ['LANG'] = language

#gettext.install(APPLICATION_NAME.lower(), LOCALE_DIR)
gettext.install('timeline')

from timelinelib.config.arguments import ApplicationArguments

application_arguments = ApplicationArguments()
application_arguments.parse_from(sys.argv[1:])

import timelinelib

timelinelib.DEBUG_ENABLED = application_arguments.get_debug_flag()

from timelinelib.wxgui.setup import setup_humblewx

setup_humblewx()

from timelinelib.wxgui.setup import start_wx_application

start_wx_application(application_arguments)
