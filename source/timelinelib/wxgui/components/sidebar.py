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

from timelinelib.wxgui.components.categorytree import CustomCategoryTree
from timelinelib.wxgui.components.labelfilter.view import LabelFilter


class Sidebar(wx.Panel):

    def __init__(self, edit_controller, parent, config):
        self._edit_controller = edit_controller
        self._config = config
        wx.Panel.__init__(self, parent, style=wx.BORDER_NONE)
        self.Hide()
        self._create_gui()

    def show_label_filtering(self):
        self._label_include_filter.Show()
        self._sizer.Layout()

    def hide_label_filtering(self):
        self._label_include_filter.hide()
        self._sizer.Layout()

    def _create_gui(self):
        self.category_tree = CustomCategoryTree(self)
        label = _("View Categories Individually")
        self.cbx_toggle_cat_view = wx.CheckBox(self, -1, label)
        self._label_include_filter = LabelFilter(self, _('Include events with labels:'))
        if not self._config.show_label_filtering:
            self._label_include_filter.hide(clear=False)
        # Layout
        self._sizer = wx.GridBagSizer(vgap=0, hgap=0)
        self._sizer.AddGrowableCol(0, proportion=0)
        self._sizer.AddGrowableRow(0, proportion=0)
        self._sizer.Add(self.category_tree, (0, 0), flag=wx.GROW)
        self._sizer.Add(self.cbx_toggle_cat_view, (1, 0), flag=wx.ALL, border=5)
        self._sizer.Add(self._label_include_filter, (2, 0), flag=wx.GROW | wx.LEFT, border=5)
        self.SetSizer(self._sizer)
        self.Bind(wx.EVT_CHECKBOX, self._cbx_on_click, self.cbx_toggle_cat_view)

    def ok_to_edit(self):
        return self._edit_controller.ok_to_edit()

    def edit_ends(self):
        return self._edit_controller.edit_ends()

    def _cbx_on_click(self, evt):
        from timelinelib.wxgui.frames.mainframe.mainframe import CatsViewChangedEvent
        event = CatsViewChangedEvent(self.GetId(), is_checked=evt.GetEventObject().IsChecked())
        self.GetEventHandler().ProcessEvent(event)
