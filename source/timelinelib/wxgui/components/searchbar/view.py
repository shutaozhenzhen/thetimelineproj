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
from timelinelib.wxgui.components.searchbar.controller import SearchBarController
from timelinelib.wxgui.components.searchbar.guicreator.guicreator import GuiCreator


class SearchBar(wx.ToolBar, GuiCreator):

    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, style=wx.TB_HORIZONTAL | wx.TB_BOTTOM)
        self._controller = SearchBarController(self)
        self._create_gui()
        self.UpdateButtons()

    def SetTimelineCanvas(self, timeline_canvas):
        self._controller.set_timeline_canvas(timeline_canvas)

    def GetValue(self):
        return self._search.GetValue()

    def GetPeriod(self):
        return self._period.GetString(self._period.GetSelection())

    def UpdateNomatchLabels(self, nomatch):
        self._lbl_no_match.Show(nomatch)

    def UpdateSinglematchLabel(self, singlematch):
        self._lbl_single_match.Show(singlematch)

    def UpdateButtons(self):
        self.EnableTool(wx.ID_BACKWARD, self._controller.enable_backward())
        self.EnableTool(wx.ID_FORWARD, self._controller.enable_forward())
        self.EnableTool(wx.ID_MORE, self._controller.enable_list())
