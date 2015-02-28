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


import os.path

import wx

from timelinelib.wxgui.utils import _ask_question
from timelinelib.wxgui.utils import WildcardHelper
from timelinelib.wxgui.utils import BORDER
from timelinelib.plugin.pluginbase import PluginBase
from timelinelib.plugin.factory import EXPORTER
import  wx.lib.mixins.listctrl  as  listmix


class ListExporter(PluginBase):

    def service(self):
        return EXPORTER

    def display_name(self):
        return _("Export to Listbox...")

#     def wxid(self):
#         from timelinelib.wxgui.dialogs.mainframe import ID_EXPORT
#         return ID_EXPORT

    def run(self, main_frame):
        dlg = ListboxDialox(self.display_name())
        dlg.populate(self.get_events(main_frame.timeline))
        dlg.ShowModal()
        dlg.Destroy()

    def get_events(self, timeline):
        return [(event.get_time_period().get_label(), event.get_text()) for event in timeline.get_all_events()]


class ListboxDialox(wx.Dialog):

    def __init__(self, title, parent=None):
        wx.Dialog.__init__(self, parent, title=title, style=wx.RESIZE_BORDER)
        self._create_gui()

    def populate(self, events):
        self.list.populate(events)

    def _create_gui(self):
        self.list = TestListCtrl(self)
        button_box = self._create_button_box()
        vbox = self._create_vbox(self.list, button_box)
        self.SetSizerAndFit(vbox)

    def _create_button_box(self):
        self.btn_close = self._create_close_btn()
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(self.btn_close, flag=wx.LEFT, border=BORDER)
        return button_box

    def _create_close_btn(self):
        btn_close = wx.Button(self, wx.ID_CLOSE)
        btn_close.SetDefault()
        btn_close.SetFocus()
        self.SetAffirmativeId(wx.ID_CLOSE)
        return btn_close

    def _create_vbox(self, ctrl, btn_box):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ctrl, flag=wx.ALL | wx.EXPAND, border=BORDER)
        vbox.Add(btn_box, flag=wx.ALL | wx.EXPAND, border=BORDER)
        return vbox


class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent, pos=wx.DefaultPosition, size=(250, 400), style=wx.LC_REPORT):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def populate(self, items):
        import sys
        self.InsertColumn(0, "Time period")
        self.InsertColumn(1, "Event")
        for period, event in items:
            index = self.InsertStringItem(sys.maxint, period, 0)
            self.SetStringItem(index, 1, event)

