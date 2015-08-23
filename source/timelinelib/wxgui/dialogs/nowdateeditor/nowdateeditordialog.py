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

from timelinelib.wxgui.utils import BORDER
from timelinelib.wxgui.utils import time_picker_for


class NowDateEditorDialog(wx.Dialog):
    """
    This dialog is used to change the "now" date.
    It is opened when the user selects the Navigate -> Open Now Date Editor 
    is selected.
    """

    def __init__(self, parent, config, db, handle_new_time_fn, title):
        wx.Dialog.__init__(self, parent, title=title)
        self.db = db
        self.handle_new_time_fn = handle_new_time_fn
        self.time_type = self.db.get_time_type()
        self.config = config
        self._create_gui()
        self.time_picker.set_value(self.db.get_saved_now())
        if self._display_checkbox_show_time():
            self.time_picker.show_time(self.checkbox.IsChecked())
        self.time_picker.SetFocus()
        self.handle_new_time_fn(self.db.get_saved_now())

    def on_escape(self):
        self.Close()

    def _create_gui(self):
        self._create_show_time_checkbox()
        self._create_time_picker()
        self._layout_components()

    def _create_show_time_checkbox(self):
        if self._display_checkbox_show_time():
            self.checkbox = wx.CheckBox(self, label=_("Show time"))
            self.checkbox.SetValue(False)
            self.Bind(wx.EVT_CHECKBOX, self._show_time_checkbox_on_checked, self.checkbox)

    def _show_time_checkbox_on_checked(self, e):
        self.time_picker.show_time(e.IsChecked())

    def _create_time_picker(self):
        self.time_picker = time_picker_for(self.time_type)(self, config=self.config, on_change=self._time_picker_on_changed)
    
    def _time_picker_on_changed(self):
        try:
            self.db.set_saved_now(self._get_timepicker_time())
            self.handle_new_time_fn(self.db.get_saved_now())
        except ValueError:
            pass
            
    def _get_timepicker_time(self):
        time = self.time_picker.get_value()
        if time is None:
            raise ValueError()
        if self._display_checkbox_show_time():
            if not self.checkbox.IsChecked():
                gt = self.time_type.get_utils().from_time(time)
                gt.hour = 12
                time=gt.to_time()
        return time        
        
    def _change_time(self,time):
        self.db.set_saved_now(time)
        self.handle_new_time_fn(time)

    def _layout_components(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        if self._display_checkbox_show_time():
            vbox.Add(self.checkbox, flag=wx.LEFT | wx.TOP | wx.RIGHT,
                     border=BORDER, proportion=1)
        if self._display_checkbox_show_time():
            flag = wx.EXPAND | wx.RIGHT | wx.BOTTOM | wx.LEFT
        else:
            flag = wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.LEFT
        vbox.Add(self.time_picker, flag=flag,
                 border=BORDER, proportion=1)
        self.SetSizerAndFit(vbox)

    def _display_checkbox_show_time(self):
        return self.time_type.is_date_time_type()
