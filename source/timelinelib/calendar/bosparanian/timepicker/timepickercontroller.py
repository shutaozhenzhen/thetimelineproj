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

from timelinelib.calendar.bosparanian.bosparanian import is_valid_time


class BosparanianTimePickerController:

    def __init__(self, time_picker, on_change):
        self.time_picker = time_picker
        self.original_bg = self.time_picker.GetBackgroundColour()
        self.separator = ":"
        self.hour_part = 0
        self.minute_part = 1
        self.last_selection = None
        self.on_change = on_change

    def get_value(self):
        try:
            split = self.time_picker._get_time_string().split(self.separator)
            if len(split) != 2:
                raise ValueError()
            hour_string, minute_string = split
            hour = int(hour_string)
            minute = int(minute_string)
            if not is_valid_time(hour, minute, 0):
                raise ValueError()
            return hour, minute, 0
        except ValueError:
            raise ValueError("Invalid time.")

    def set_value(self, value):
        hour, minute, _ = value
        time_string = "%02d:%02d" % (hour, minute)
        self.time_picker.set_time_string(time_string)
        self._on_change()

    def _on_change(self):
        if self._time_is_valid() and not self.on_change is None:
            self.on_change()

    def on_set_focus(self):
        if self.last_selection:
            start, end = self.last_selection
            self.time_picker.SetSelection(start, end)
        else:
            self._select_part(self.hour_part)

    def on_kill_focus(self):
        self.last_selection = self.time_picker.GetSelection()

    def on_tab(self):
        if self._in_minute_part():
            return True
        self._select_part(self.minute_part)
        return False

    def on_shift_tab(self):
        if self._in_hour_part():
            return True
        self._select_part(self.hour_part)
        return False

    def on_text_changed(self):
        try:
            self.get_value()
            self.time_picker.SetBackgroundColour(self.original_bg)
        except ValueError:
            self.time_picker.SetBackgroundColour("pink")
        self.time_picker.Refresh()

    def on_up(self):
        def increment_hour(time):
            hour, minute, second = time
            new_hour = hour + 1
            if new_hour > 23:
                new_hour = 0
            return new_hour, minute, second

        def increment_minutes(time):
            hour, minute, second = time
            new_hour = hour
            new_minute = minute + 1
            if new_minute > 59:
                new_minute = 0
                new_hour = hour + 1
                if new_hour > 23:
                    new_hour = 0
            return new_hour, new_minute, second

        if not self._time_is_valid():
            return
        selection = self.time_picker.GetSelection()
        current_time = self.get_value()
        if self._in_hour_part():
            new_time = increment_hour(current_time)
        else:
            new_time = increment_minutes(current_time)
        if current_time != new_time:
            self._set_new_time_and_restore_selection(new_time, selection)
        self._on_change()

    def on_down(self):
        def decrement_hour(time):
            hour, minute, second = time
            new_hour = hour - 1
            if new_hour < 0:
                new_hour = 23
            return new_hour, minute, second

        def decrement_minutes(time):
            hour, minute, second = time
            new_hour = hour
            new_minute = minute - 1
            if new_minute < 0:
                new_minute = 59
                new_hour = hour - 1
                if new_hour < 0:
                    new_hour = 23
            return new_hour, new_minute, second

        if not self._time_is_valid():
            return
        selection = self.time_picker.GetSelection()
        current_time = self.get_value()
        if self._in_hour_part():
            new_time = decrement_hour(current_time)
        else:
            new_time = decrement_minutes(current_time)
        if current_time != new_time:
            self._set_new_time_and_restore_selection(new_time, selection)
        self._on_change()

    def _set_new_time_and_restore_selection(self, new_time, selection):
        def restore_selection(selection):
            self.time_picker.SetSelection(selection[0], selection[1])
        self.set_value(new_time)
        restore_selection(selection)

    def _time_is_valid(self):
        try:
            self.get_value()
        except ValueError:
            return False
        return True

    def _select_part(self, part):
        if self._separator_pos() == -1:
            return
        if part == self.hour_part:
            self.time_picker.SetSelection(0, self._separator_pos())
        else:
            time_string_len = len(self.time_picker._get_time_string())
            self.time_picker.SetSelection(self._separator_pos() + 1, time_string_len)
        self.preferred_part = part

    def _in_hour_part(self):
        if self._separator_pos() == -1:
            return
        return self.time_picker.GetInsertionPoint() <= self._separator_pos()

    def _in_minute_part(self):
        if self._separator_pos() == -1:
            return
        return self.time_picker.GetInsertionPoint() > self._separator_pos()

    def _separator_pos(self):
        return self.time_picker._get_time_string().find(self.separator)
