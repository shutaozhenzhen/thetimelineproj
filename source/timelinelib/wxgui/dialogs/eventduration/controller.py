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
from timelinelib.wxgui.framework import Controller
from timelinelib.canvas.data.timeperiod import TimePeriod


PRECISION_CHOICES = ['0', '1', '2', '3', '4', '5']


class EventsDurationController(Controller):

    def on_init(self, db, config, preferred_category_name):
        self._db = db
        self._config = config
        self._populate_view(preferred_category_name)
        self._calculate()

    def on_use_start_period(self, evt):
        self.view.EnableStartTime(evt.EventObject.Value)
        self._calculate()

    def on_use_end_period(self, evt):
        self.view.EnableEndTime(evt.EventObject.Value)
        self._calculate()

    def on_copy(self, evt):
        self._copy_to_clipboard()

    def recalculate(self, evt=None):
        self._calculate()

    def _populate_view(self, preferred_category_name):
        self.view.PopulateCategories(exclude=None)
        self.view.SelectCategory(0)
        self.view.SelectPrecision(1)
        self.view.SetCopyToClipboard(False)
        self.view.SetDurationTypeChoices(self._db.get_time_type().get_duration_types())
        self.view.SetStartTime(None)
        self.view.SetEndTime(None)
        self.view.EnableStartTime(False)
        self.view.EnableEndTime(False)
        self.view.SetPreferredCategory(preferred_category_name or self.view.ALL_CATEGORIES)

    def _calculate(self):
        events = self._get_events()
        duration = self._calculate_duration(events)
        self.view.SetDurationResult(str(duration))
        self._autocopy_to_clipboard()

    def _get_events(self):
        category = self.view.GetCategory()
        events = self._db.get_all_events()
        if category is not None:
            events = [e for e in events
                      if e.get_category()
                      and self._after_or_at_start(e)
                      and self._before_or_at_end(e)
                      and self._include(category.name, e.get_category())]
        else:
            events = [e for e in events
                      if self._after_or_at_start(e)
                      and self._before_or_at_end(e)]
        return events

    def _include(self, category_name, event_category):
        if event_category.name == category_name:
            return True
        else:
            if event_category.parent:
                return self._include(category_name, event_category.parent)
            else:
                return False

    def _after_or_at_start(self, event):
        if self.view.GetStartTime():
            return event.get_end_time() >= self.view.GetStartTime()
        return True

    def _before_or_at_end(self, event):
        if self.view.GetEndTime():
            return event.get_start_time() <= self.view.GetEndTime()
        return True

    def _calculate_duration(self, events):
        duration = sum([self._get_event_duration(e) for e in events])
        precision = self.view.GetPrecision()
        divisor = self._db.get_time_type().get_duration_divisor(self.view.GetDurationType(), self._config.workday_length)
        if precision == 0:
            return duration // divisor
        else:
            return round(duration / divisor, precision)

    def _get_event_duration(self, e):
        start_time = max(self.view.GetStartTime() or e.get_start_time(), e.get_start_time())
        end_time = self._get_end_time(e)
        if end_time < start_time:
            return 0
        return TimePeriod(start_time, end_time).duration().value

    def _get_end_time(self, e):
        if e.ends_today:
            end_time = self._db.get_time_type().now()
        else:
            end_time = e.get_end_time()
        return min(self.view.GetEndTime() or end_time, end_time)

    def _autocopy_to_clipboard(self):
        if self.view.GetCopyToClipboard():
            self._copy_to_clipboard()

    def _copy_to_clipboard(self):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.view.GetDurationResult()))
            wx.TheClipboard.Close()
