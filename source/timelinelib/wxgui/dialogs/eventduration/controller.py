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


DURATION_TYPE_HOURS = _('Hours')
DURATION_TYPE_WORKDAYS = _('Workdays')
DURATION_TYPE_DAYS = _('Days')
DURATION_TYPE_MINUTES = _('Minutes')
DURATION_TYPE_SECONDS = _('Seconds')

DURATION_TYPES_CHOICES = [
    DURATION_TYPE_HOURS,
    DURATION_TYPE_WORKDAYS,
    DURATION_TYPE_DAYS,
    DURATION_TYPE_MINUTES,
    DURATION_TYPE_SECONDS]
PRECISION_CHOICES = ['0', '1', '2', '3', '4', '5']


class EventsDurationController(Controller):

    def on_init(self, db, category):
        self._db = db
        self._category = category
        self._populate_view()

    def on_ok_clicked(self, event):
        events = self._get_events()
        duration = self._calculate_duration(events)
        self.view.SetDuration(str(duration))
        self._copy_to_clipboard()

    def _get_events(self):
        category = self.view.GetCategory()
        events = self._db.get_all_events()
        if category is not None:
            events = [e for e in events if self._include(category.name, e.get_category())]
        return events

    def _include(self, category_name, event_category):
        if event_category.name != category_name:
            if event_category.parent:
                return self._include(category_name, event_category.parent)
            else:
                return False
        else:
            return True

    def _calculate_duration(self, events):
        duration = sum([e.get_time_period().duration().seconds for e in events])
        precision = self.view.GetPrecision()
        if precision == 0:
            return duration // self._get_divisor()
        else:
            return round(duration / self._get_divisor(), precision)

    def _get_divisor(self):
        return {
            DURATION_TYPE_SECONDS: 1,
            DURATION_TYPE_MINUTES: 60,
            DURATION_TYPE_HOURS: 3600,
            DURATION_TYPE_DAYS: 86400,
            DURATION_TYPE_WORKDAYS: 28800,
        }[self.view.GetDurationType()]

    def _populate_view(self):
        self.view.PopulateCategories(exclude=None)
        self.view.SelectCategory(0)
        self.view.SelectPrecision(1)
        self.view.SetCopyToClipboard(True)

    def _copy_to_clipboard(self):
        if wx.TheClipboard.Open() and self.view.GetCopyToClipboard():
            wx.TheClipboard.SetData(wx.TextDataObject(self.view.GetDurationResult()))
            wx.TheClipboard.Close()