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

from timelinelib.wxgui.dialogs.eventlist.view import EventListDialog


class SearchBarController(object):

    def __init__(self, view):
        self.view = view
        self.result = []
        self.result_index = 0
        self.last_search = None
        self.last_period = None

    def SetTimelineCanvas(self, timeline_canvas):
        self.timeline_canvas = timeline_canvas
        self.view.Enable(timeline_canvas is not None)

    def Search(self):
        new_search = self.view.GetValue()
        new_period = self.view.GetPeriod()
        if (
            (self.last_search is not None and self.last_search == new_search) and 
            (self.last_period is not None and self.last_period == new_period)):
            self.Next()
        else:
            self.last_search = new_search
            self.last_period = new_period
            if self.timeline_canvas is not None:
                self.result = self.timeline_canvas.GetFilteredEvents(new_search)
            else:
                self.result = []
            self.result_index = 0
            self.navigate_to_match()
            self.view.UpdateNomatchLabels(len(self.result) == 0)
            self.view.UpdateSinglematchLabel(len(self.result) == 1)
        self.view.UpdateButtons()

    def Next(self):
        if not self._on_last_match():
            self.result_index += 1
            self.navigate_to_match()
            self.view.UpdateButtons()

    def Prev(self):
        if not self._on_first_match():
            self.result_index -= 1
            self.navigate_to_match()
            self.view.UpdateButtons()

    def List(self):
        event_list = [event.get_label(self.timeline_canvas.GetTimeType()) for event in self.result]
        dlg = EventListDialog(self.view, event_list)
        if dlg.ShowModal() == wx.ID_OK:
            self.result_index = dlg.GetSelectedIndex()
            self.navigate_to_match()
        dlg.Destroy()

    def navigate_to_match(self):
        if (self.timeline_canvas is not None and self.result_index in range(len(self.result))):
            event = self.result[self.result_index]
            self.timeline_canvas.Navigate(lambda tp: tp.center(event.mean_time()))
            self.timeline_canvas.HighligtEvent(event, clear=True)

    def enable_backward(self):
        return bool(self.result and self.result_index > 0)

    def enable_forward(self):
        return bool(self.result and self.result_index < (len(self.result) - 1))

    def enable_list(self):
        return bool(len(self.result) > 0)

    def _on_first_match(self):
        return self.result > 0 and self.result_index == 0

    def _on_last_match(self):
        return self.result > 0 and self.result_index == (len(self.result) - 1)


