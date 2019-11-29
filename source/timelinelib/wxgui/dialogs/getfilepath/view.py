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

FUNC_OPEN = 1
FUNC_SAVE_AS = 2
FUNC_NEW = 3


class GetFilePath(wx.FileDialog):

    STYLES = {
        FUNC_OPEN: wx.FD_OPEN,
        FUNC_SAVE_AS: wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        FUNC_NEW: wx.FD_SAVE
    }

    TITLES = {
        FUNC_OPEN: _("Open Timeline"),
        FUNC_SAVE_AS:  _("Save Timeline As"),
        FUNC_NEW: _("Create Timeline"),
    }

    def __init__(self, parent, func, current_path):
        self._controller = GetFilePathContoller(self, current_path)
        wx.FileDialog.__init__(self,
                               parent,
                               message=self.TITLES[func],
                               defaultDir=self._controller.default_dir,
                               wildcard=self._controller.wildcards,
                               style=self.STYLES[func])

    @property
    def new_path(self):
        return self._controller.new_path()


def open_get_file_path_dialog(parent, func, current_path):
    dialog = GetFilePath(parent, func, current_path)
    if dialog.ShowModal() == wx.ID_OK:
        new_timeline_path = dialog.new_path
    else:
        new_timeline_path = None
    dialog.Destroy()
    return new_timeline_path
