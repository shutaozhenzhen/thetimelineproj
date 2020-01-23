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


from timelinelib.calendar.bosparanian.bosparanian import BosparanianDateTime


class BosparanianDateTimePickerController:

    def __init__(self, date_picker, time_picker, now_fn, on_change=None):
        self.date_picker = date_picker
        self.time_picker = time_picker
        self.now_fn = now_fn
        self._on_change = on_change

    def get_value(self):
        if self.time_picker.IsShown():
            hour, minute, second = self.time_picker.GetTime()
        else:
            hour, minute, second = (0, 0, 0)
        year, month, day = self.date_picker.get_value()
        return BosparanianDateTime(year, month, day, hour, minute, second).to_time()

    def set_value(self, time):
        if time is None:
            time = self.now_fn()
        self.date_picker.set_value(BosparanianDateTime.from_time(time).to_date_tuple())
        self.time_picker.SetTime(BosparanianDateTime.from_time(time).to_time_tuple())
        self.changed()

    def changed(self):
        if self._on_change is not None:
            self._on_change()