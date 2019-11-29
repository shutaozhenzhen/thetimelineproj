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


import wx
from timelinelib.wxgui.dialogs.getfilepath.controller import GetFilePathContoller

class GetFilePath(wx.FileDialog):

    STYLE = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT

    def __init__(self, parent, current_path, message):
        self._controller = GetFilePathContoller(self, current_path)
        wx.FileDialog.__init__(self,
                               parent,
                               message=message,
                               defaultDir=self._controller.default_dir,
                               wildcard=self._controller.wildcards,
                               style=self.STYLE)

    @property
    def new_path(self):
        return self._controller.new_path()


def open_get_file_path_dialog(parent, current_path, message):
    dialog = GetFilePath(parent, current_path, message)
    if dialog.ShowModal() == wx.ID_OK:
        new_timeline_path = dialog.new_path
    else:
        new_timeline_path = None
    dialog.Destroy()
    return new_timeline_path
