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

from timelinelib.wxgui.dialogs.timeeditor.timeeditordialogcontroller import TimeEditorDialogController
from timelinelib.wxgui.framework import Dialog


class TimeEditorDialog(Dialog):

    """
    <BoxSizerVertical>
        <CheckBox use="$(use_checkbox)" label="$(cb_text)" id="cbx_show_time"
                  border="LEFT|TOP"
                  event_EVT_CHECKBOX="show_time_checkbox_on_checked" />
        <TimePicker border="LEFT|RIGHT|TOP" id="time_picker"/>
        <StdDialogButtonSizer
            buttons="OK|CANCEL"
            border="ALL"
            event_EVT_BUTTON="ok_button_clicked|ID_OK"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, config, time_type, time, title):
        self.time_type = time_type
        self.config = config
        Dialog.__init__(self, TimeEditorDialogController, parent, {
            "cb_text": _("Show time"),
            "use_checkbox": self.time_type.is_date_time_type()
        }, title=title)
        self.controller.on_init(self.time_type, time)

    def SetTime(self, time):
        self.time_picker.set_value(time)

    def GetTime(self):
        return self.time_picker.get_value()

    def ShowTimeIsChecked(self):
        return self.cbx_show_time.IsChecked()

    def ShowTime(self, value):
        try:
            self.time_picker.show_time(value)
        except:
            pass

    def Close(self):
        self.EndModal(wx.ID_OK)
