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

import os
from timelinelib.wxgui.utils import WildcardHelper
from timelinelib.wxgui.framework import Controller


class GetFilePathContoller(Controller):

    def __init__(self, view, current_path):
        self._view = view
        self._default_dir = os.path.dirname(current_path)
        self._wildcard_helper = WildcardHelper(_("Timeline files"), ["timeline"])

    @property
    def default_dir(self):
        return self._default_dir

    @property
    def wildcards(self):
        return self._wildcard_helper.wildcard_string()

    def new_path(self):
        return self._wildcard_helper.get_path(self._view)
