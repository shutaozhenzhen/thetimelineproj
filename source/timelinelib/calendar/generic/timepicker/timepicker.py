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


from timelinelib.wxgui.components import TextPatternControl


class TimePicker(TextPatternControl):

    HOUR_GROUP = 0
    MINUTE_GROUP = 1
    SECOND_GROUP = 2

    def __init__(self, parent, use_second, separators, validator_function=None):
        self._parent = parent
        self._use_second = use_second
        if use_second:
            fit_text = f"00{separators[0]}00{separators[1]}00"
        else:
            fit_text = f"00{separators[0]}00"
        self._validator_function = validator_function
        TextPatternControl.__init__(self, parent, fit_text=fit_text)
        self.SetSeparators(separators)
        self.SetValidator(self._is_time_valid)
        self.SetUpHandler(self.HOUR_GROUP, self._increment_hour)
        self.SetUpHandler(self.MINUTE_GROUP, self._increment_minute)
        self.SetDownHandler(self.HOUR_GROUP, self._decrement_hour)
        self.SetDownHandler(self.MINUTE_GROUP, self._decrement_minute)
        self.SetUpHandler(self.SECOND_GROUP, self._increment_second)
        self.SetDownHandler(self.SECOND_GROUP, self._decrement_second)

    def GetTime(self):
        return self.parts_to_time(self.GetParts())

    def SetTime(self, time):
        self.SetParts(self.time_to_parts(time))

    def time_is_invalid(self, hour, minute, second):
        if self._validator_function != None:
            return not self._validator_function(hour, minute, second)
        raise NotImplementedError()

    def _is_time_valid(self):
        try:
            self.GetTime()
        except ValueError:
            return False
        else:
            return True

    def _increment_hour(self):
        self.SetTime(increment_hour(self.GetTime()))

    def _increment_minute(self):
        self.SetTime(increment_minute(self.GetTime()))

    def _increment_second(self):
        self.SetTime(increment_second(self.GetTime()))

    def _decrement_hour(self):
        self.SetTime(decrement_hour(self.GetTime()))

    def _decrement_minute(self):
        self.SetTime(decrement_minute(self.GetTime()))

    def _decrement_second(self):
        self.SetTime(decrement_second(self.GetTime()))

    def parts_to_time(self, parts):
        hour = minute = second = 0
        if not self._use_second:
            [hour_str, minute_str] = parts
            hour = int(hour_str)
            minute = int(minute_str)
        if self._use_second and parts:
            [hour_str, minute_str, second_str] = parts
            hour = int(hour_str)
            minute = int(minute_str)
            second = int(second_str)
        if self.time_is_invalid(hour, minute, second):
            raise ValueError()
        return hour, minute, second

    def time_to_parts(self, time):
        (hour, minute, second) = time
        if self._use_second:
            return [
                "%02d" % hour,
                "%02d" % minute,
                "%02d" % second,
            ]
        else:
            return [
                "%02d" % hour,
                "%02d" % minute
            ]


def increment_hour(time):
    hour, minute, second = time
    new_hour = hour + 1
    if new_hour > 23:
        new_hour = 0
    return new_hour, minute, second


def increment_minute(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute + 1
    if new_minute > 59:
        new_minute = 0
        new_hour = hour + 1
        if new_hour > 23:
            new_hour = 0
    return new_hour, new_minute, second


def increment_second(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute
    new_second = second
    if new_second > 59:
        new_second = 0
        new_minute = minute + 1
        if new_minute > 59:
            new_minute = 0
            new_hour = hour + 1
            if new_hour > 23:
                new_hour = 0
    return new_hour, new_minute, new_second


def decrement_hour(time):
    hour, minute, second = time
    new_hour = hour - 1
    if new_hour < 0:
        new_hour = 23
    return new_hour, minute, second


def decrement_minute(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute - 1
    if new_minute < 0:
        new_minute = 59
        new_hour = hour - 1
        if new_hour < 0:
            new_hour = 23
    return new_hour, new_minute, second


def decrement_second(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute
    new_second = second
    if new_second < 0:
        new_second = 59
        new_minute = minute - 1
        if new_minute < 0:
            new_minute = 59
            new_hour = hour - 1
            if new_hour < 0:
                new_hour = 23
    return new_hour, new_minute, new_second