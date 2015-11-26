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


import wx

from timelinelib.test.cases.unit import UnitTestCase


class WxComponentTestCase(UnitTestCase):

    def setUp(self):
        self._app = wx.App(False)
        self._main_frame = wx.Frame(None)
        self._main_frame.Bind(wx.EVT_CLOSE, self._main_frame_on_close)
        self._main_panel = wx.Panel(self._main_frame)
        self._components = []
        self._component_by_name = {}
        self._is_close_called = False

    def tearDown(self):
        self._close()

    def add_component(self, name, cls, *args):
        self._component_by_name[name] = cls(self._main_panel, *args)
        self._components.append(self._component_by_name[name])

    def add_button(self, text, callback, component_name=None):
        button = wx.Button(self._main_panel, label=text)
        self._components.append(button)

        def event_listener(event):
            if component_name:
                callback(self.get_component(component_name))
            else:
                callback()
        button.Bind(wx.EVT_BUTTON, event_listener)

    def add_separator(self):
        label = "----- separator -----"
        self._components.append(wx.StaticText(self._main_panel, label=label))

    def get_component(self, name):
        return self._component_by_name[name]

    def show_test_window(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for component in self._components:
            sizer.Add(component, flag=wx.ALL | wx.GROW, border=3)
        self._main_panel.SetSizer(sizer)
        self._main_frame.Show()
        wx.CallLater(100, self._MainLoop)

    def _MainLoop(self):
        if not self.HALT_GUI:
            wx.CallAfter(self._close)
        self._app.MainLoop()
        
    def _main_frame_on_close(self, event):
        self._is_close_called = True
        self._main_frame.Destroy()

    def _close(self):
        if not self._is_close_called:
            self._main_frame.Close()
            self._is_close_called = True
