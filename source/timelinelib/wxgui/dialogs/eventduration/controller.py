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


from timelinelib.wxgui.framework import Controller


class EventsDurationController(Controller):

    def on_init(self, db, category):
        self._db = db
        self._category = category
        self._populate_view()

    def on_ok_clicked(self, event):
        events = self._get_events()
        duration = self._calculate_duration(events)
        self.view.SetDuration(str(duration))

    def _get_events(self):
        category = self.view.GetCategory()
        events = self._db.get_all_events()
        if category is not None:
            events = [e for e in events if e.get_category_name() == category.name]
        return events

    def _calculate_duration(self, events):
        duration = 0
        for e in events:
            duration += e.get_time_period().duration().seconds
        duration_type = self.view.GetDurationType()
        if duration_type == 'hours':
            duration = duration // 3600
        elif duration_type == 'minutes':
            duration = duration // 60
        elif duration_type == 'workdays':
            duration = duration // 3600 // 8
        elif duration_type == 'days':
            duration = duration // 3600 // 24
        return duration

    def _populate_view(self):
        self.view.PopulateCategories(exclude=None)
