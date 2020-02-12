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

from timelinelib.wxgui.components.labelfilter.controller import LabelFilterController


class LabelFilter(wx.Panel):

    def __init__(self, parent, text):
        wx.Panel.__init__(self, parent)
        self._create_controls(text)
        self._controller = LabelFilterController(self)

    def get_labels(self):
        return self._text_control.GetValue().split()

    def match_all(self):
        return self._rb_match_all.GetValue()

    def hide(self, clear=True):
        if clear:
            self._text_control.SetValue('')
            self._txt_on_enter(None)
        self.Hide()

    def visible(self, event):
        return self._controller.visible(event)

    def _create_controls(self, text):
        static_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, text), wx.VERTICAL)
        static_box_sizer.Add(self._create_text_control(), flag=wx.GROW)
        static_box_sizer.Add(self._create_rb_control())
        self.SetSizer(static_box_sizer)

    def _create_text_control(self):
        self._text_control = wx.TextCtrl(self, -1, style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self._txt_on_enter, self._text_control)
        return self._text_control

    def _create_rb_control(self):
        rb_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._rb_match_one = wx.RadioButton(self, wx.ID_ANY, label=_('Match any label'), style=wx.RB_GROUP)
        self._rb_match_all = wx.RadioButton(self, wx.ID_ANY, label=_('Match all labels'))
        rb_sizer.Add(self._rb_match_one)
        rb_sizer.Add(self._rb_match_all)
        self.Bind(wx.EVT_RADIOBUTTON, self._txt_on_enter, self._rb_match_one)
        self.Bind(wx.EVT_RADIOBUTTON, self._txt_on_enter, self._rb_match_all)
        return rb_sizer

    def _txt_on_enter(self, evt):
        from timelinelib.wxgui.frames.mainframe.mainframe import LabelsChangedEvent
        event = LabelsChangedEvent(self.GetId(), filter_labels_controller=self._controller)
        self.GetEventHandler().ProcessEvent(event)
