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
Defining paths for resources needed by the application.
"""

import os.path


_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

if _ROOT.endswith('dist'):
    ICONS_DIR = os.path.join(_ROOT, 'timeline', u"icons")
    EVENT_ICONS_DIR = os.path.join(_ROOT, 'timeline', u"icons", u"event_icons")
    LOCALE_DIR = os.path.join(_ROOT, 'timeline', u"translations")
    HELP_RESOURCES_DIR = os.path.join(_ROOT, 'timeline', u"help_resources")
    print('ICONS_DIR', ICONS_DIR)
    print('EVENT_ICONS_DIR', EVENT_ICONS_DIR)
    print('LOCALE_DIR', LOCALE_DIR)
    print('HELP_RESOURCES_DIR', HELP_RESOURCES_DIR)
else:
    ICONS_DIR = os.path.join(_ROOT, u"icons")
    EVENT_ICONS_DIR = os.path.join(_ROOT, u"icons", u"event_icons")
    LOCALE_DIR = os.path.join(_ROOT, u"translations")
    HELP_RESOURCES_DIR = os.path.join(_ROOT, u"help_resources")

