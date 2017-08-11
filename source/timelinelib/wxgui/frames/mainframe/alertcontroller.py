# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


class AlertController(object):

    def display_events_alerts(self, all_events, time_type):
        self.time_type = time_type
        for event in all_events:
            alert = event.get_data("alert")
            if alert is not None:
                if self._time_has_expired(alert[0]):
                    self._display_and_delete_event_alert(event, alert)

    def _display_and_delete_event_alert(self, event, alert):
        self._display_alert_dialog(alert, event)
        event.set_data("alert", None)

    def _alert_time_as_text(self, alert):
        return "%s" % alert[0]

    def _time_has_expired(self, time):
        return time <= self.time_type.now()

    def _display_alert_dialog(self, alert, event):
        text = self._format_alert_text(alert, event)
        dialog = TextDisplayDialog("Alert", text)
        dialog.SetWindowStyleFlag(dialog.GetWindowStyleFlag() | wx.STAY_ON_TOP)
        wx.Bell()
        dialog.ShowModal()
        dialog.Destroy()

    def _format_alert_text(self, alert, event):
        text1 = "Trigger time: %s\n\n" % alert[0]
        text2 = "Event: %s\n\n" % event.get_label(self.time_type)
        text = "%s%s%s" % (text1, text2, alert[1])
        return text