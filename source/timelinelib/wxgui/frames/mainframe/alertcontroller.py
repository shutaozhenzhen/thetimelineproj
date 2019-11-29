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

from timelinelib.wxgui.dialogs.textdisplay.view import TextDisplayDialog
from timelinelib.wxgui.timer import TimelineTimer


class AlertController:

    def __init__(self, main_frame):
        self._main_frame = main_frame
        self._timeline = main_frame.timeline
        self._timer = None
        self._alert_dialog_open = False

    def start_timer(self):
        self._timer = TimelineTimer(self._main_frame)
        self._timer.register(self._timer_tick)
        self._timer.start(10000)
        return self

    def stop_timer(self):
        self._timer.stop()

    def _timer_tick(self, evt):
        if self._timeline is None:
            return
        if self._alert_dialog_open:
            return
        self._display_events_alerts()
        self._alert_dialog_open = False

    def _display_events_alerts(self):
        self._alert_dialog_open = True
        all_events = self._timeline.get_all_events()
        self.display_events_alerts(all_events, self._timeline.get_time_type())

    def display_events_alerts(self, all_events, time_type, dialog=None):
        self._active = True
        self._dialog = dialog
        self.time_type = time_type
        for event in [event for event in all_events if event.get_data("alert") is not None]:
            alert = event.get_data("alert")
            if self._time_has_expired(alert[0]):
                self._display_and_delete_event_alert(event, alert)

    def _display_and_delete_event_alert(self, event, alert):
        self._display_alert_dialog(alert, event)
        event.set_data("alert", None)
        if self._main_frame.ok_to_edit():
            try:
                event.save()
            finally:
                self._main_frame.edit_ends()

    def _time_has_expired(self, time):
        return time <= self.time_type.now()

    def _display_alert_dialog(self, alert, event):
        text = self._format_alert_text(alert, event)
        if self._dialog is None:
            self._dialog = TextDisplayDialog("Alert")
            wx.Bell()
        self._dialog.SetText(text)
        self._dialog.SetWindowStyleFlag(self._dialog.GetWindowStyleFlag() | wx.STAY_ON_TOP)
        self._dialog.ShowModal()
        self._dialog.Destroy()

    def _format_alert_text(self, alert, event):
        text1 = "Trigger time: %s\n\n" % alert[0]
        text2 = "Event: %s\n\n" % event.get_label(self.time_type)
        text = "%s%s%s" % (text1, text2, alert[1])
        return text
