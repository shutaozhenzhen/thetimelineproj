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

from timelinelib.calendar.bosparanian.timepicker.timepickercontroller import BosparanianTimePickerController


class BosparanianTimePicker(wx.TextCtrl):

    def __init__(self, parent, on_change):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_PROCESS_ENTER)
        self.controller = BosparanianTimePickerController(self, on_change)
        self._bind_events()
        self._resize_to_fit_text()
        self.parent = parent

    def get_value(self):
        return self.controller.get_value()

    def set_value(self, value):
        self.controller.set_value(value)

    def _get_time_string(self):
        return self.GetValue()

    def set_time_string(self, time_string):
        self.SetValue(time_string)

    def _bind_events(self):

        def on_char(evt):
            if evt.GetKeyCode() == wx.WXK_TAB:
                if evt.ShiftDown():
                    skip = self.controller.on_shift_tab()
                else:
                    skip = self.controller.on_tab()
            else:
                skip = True
            evt.Skip(skip)
        self.Bind(wx.EVT_CHAR, on_char)

        def on_text(evt):
            self.controller.on_text_changed()
        self.Bind(wx.EVT_TEXT, on_text)

        def on_key_down(evt):
            if evt.GetKeyCode() == wx.WXK_UP:
                self.controller.on_up()
            elif evt.GetKeyCode() == wx.WXK_DOWN:
                self.controller.on_down()
            elif (evt.GetKeyCode() == wx.WXK_NUMPAD_ENTER or
                  evt.GetKeyCode() == wx.WXK_RETURN):
                self.parent.on_return()
            elif evt.GetKeyCode() == wx.WXK_ESCAPE:
                self.parent.on_escape()
            else:
                evt.Skip()
        self.Bind(wx.EVT_KEY_DOWN, on_key_down)

    def _resize_to_fit_text(self):
        w, _ = self.GetTextExtent("00:00")
        width = w + 20
        self.SetMinSize((width, -1))


