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


import sys


class CalendarPopupController:
    """
    All this code is to avoid system error popups, because the wx.CalendarCtrl
    object is not working correctly.
    """
    def __init__(self, view):
        self._view = view
        self._original_excepthook = sys.excepthook
        sys.excepthook = self.unhandled_exception_hook

    def on_dismiss(self):
        sys.excepthook = self._original_excepthook

    def unhandled_exception_hook(self, exception_type, value, tb):
        if exception_type != SystemError:
            self._original_excepthook(exception_type, value, tb)
        else:
            self._view.SelectionChanged()
