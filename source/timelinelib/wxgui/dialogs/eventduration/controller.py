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


PRECISION_CHOICES = ['0', '1', '2', '3', '4', '5']


class EventsDurationController(Controller):

    def on_init(self, db, config, preferred_category_name):
        self._db = db
        self._config = config
        self._populate_view(preferred_category_name)
        self.on_ok_clicked(None)

    def on_use_start_period(self, evt):
        self.view.EnableStartTime(evt.EventObject.Value)
        self.recalculate(None)

    def on_use_end_period(self, evt):
        self.view.EnableEndTime(evt.EventObject.Value)
        self.recalculate(None)

    def on_ok_clicked(self, event):
        events = self._get_events()
        duration = self._calculate_duration(events)
        self.view.SetDurationResult(str(duration))
        self._copy_to_clipboard()

    def recalculate(self, evt):
        self.on_ok_clicked(None)

    def _get_events(self):
        category = self.view.GetCategory()
        events = self._db.get_all_events()
        if category is not None:
            events = [e for e in events
                      if e.get_category()
                      and self._after_or_at_start(e)
                      and self._before_or_at_end(e)
                      and self._include(category.name, e.get_category())]
        return events

    def _include(self, category_name, event_category):
        if event_category.name != category_name:
            if event_category.parent:
                return self._include(category_name, event_category.parent)
            else:
                return False
        else:
            return True

    def _after_or_at_start(self, event):
        start_time = self.view.GetStartTime()
        if start_time:
            return event.time_period.end_time >= start_time
        return True

    def _before_or_at_end(self, event):
        end_time = self.view.GetEndTime()
        if end_time:
            return event.time_period.start_time <= end_time
        return True

    def _calculate_duration(self, events):
        duration = sum([e.get_time_period().duration().value for e in events])
        precision = self.view.GetPrecision()
        divisor = self._db.get_time_type().get_duration_divisor(self.view.GetDurationType(), self._config.workday_length)
        if precision == 0:
            return duration // divisor
        else:
            return round(duration / divisor, precision)

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
        self._set_preferred_category(preferred_category_name)

    def _set_preferred_category(self, preferred_category_name):
        if preferred_category_name:
            self.view.SetPreferredCategory(preferred_category_name.strip())
        else:
            self.view.SetPreferredCategory(self.view.ALL_CATEGORIES)

    def _copy_to_clipboard(self):
        if wx.TheClipboard.Open() and self.view.GetCopyToClipboard():
            wx.TheClipboard.SetData(wx.TextDataObject(self.view.GetDurationResult()))
            wx.TheClipboard.Close()