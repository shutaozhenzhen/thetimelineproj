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


def make_sure_timelinelib_can_be_imported():
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))
make_sure_timelinelib_can_be_imported()

def install_gettext_in_builtin_namespace():
    def _(message):
        return message
    import __builtin__
    if not "_" in __builtin__.__dict__:
        __builtin__.__dict__["_"] = _
install_gettext_in_builtin_namespace()


import wx

from timelinelib.canvas import TimelineCanvas


class EmptyCanvas(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, size=(800, 400))
        self.canvas = TimelineCanvas(self)


def show_frame(frame_class):
    app = wx.App()
    frame = frame_class()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    show_frame(EmptyCanvas)
