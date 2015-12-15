# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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


from timelinelib.calendar.gregorian import GregorianUtils
from timelinelib.wxgui.components import TextPatternControl


class GregorianTimePicker(TextPatternControl):

    HOUR_GROUP = 0
    MINUTE_GROUP = 1

    def __init__(self, parent):
        TextPatternControl.__init__(self, parent)
        self.SetSeparators([":"])
        self.SetValuesValidator(self._is_time_valid)
        self.SetUpHandler(self._increment_time)
        self.SetDownHandler(self._decrement_time)
        self._resize_to_fit_text()

    def GetGregorianTime(self):
        try:
            [hour_str, minute_str] = self.GetValues()
            hour = int(hour_str)
            minute = int(minute_str)
            if not GregorianUtils.is_valid_time(hour, minute, 0):
                raise ValueError()
            return (hour, minute, 0)
        except:
            raise ValueError("Invalid time")

    def SetGregorianTime(self, value):
        (hour, minute, second) = value
        self.SetValues(["%02d" % hour, "%02d" % minute])

    def _is_time_valid(self):
        try:
            self.GetGregorianTime()
        except ValueError:
            return False
        else:
            return True

    def _increment_time(self):
        if self.GetSelectedGroup() == self.HOUR_GROUP:
            self.SetGregorianTime(increment_hour(self.GetGregorianTime()))
        elif self.GetSelectedGroup() == self.MINUTE_GROUP:
            self.SetGregorianTime(increment_minutes(self.GetGregorianTime()))

    def _decrement_time(self):
        if self.GetSelectedGroup() == self.HOUR_GROUP:
            self.SetGregorianTime(decrement_hour(self.GetGregorianTime()))
        elif self.GetSelectedGroup() == self.MINUTE_GROUP:
            self.SetGregorianTime(decrement_minutes(self.GetGregorianTime()))

    def _resize_to_fit_text(self):
        w, _ = self.GetTextExtent("00:00")
        width = w + 20
        self.SetMinSize((width, -1))


def increment_hour(time):
    hour, minute, second = time
    new_hour = hour + 1
    if new_hour > 23:
        new_hour = 0
    return (new_hour, minute, second)


def increment_minutes(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute + 1
    if new_minute > 59:
        new_minute = 0
        new_hour = hour + 1
        if new_hour > 23:
            new_hour = 0
    return (new_hour, new_minute, second)


def decrement_hour(time):
    hour, minute, second = time
    new_hour = hour - 1
    if new_hour < 0:
        new_hour = 23
    return (new_hour, minute, second)


def decrement_minutes(time):
    hour, minute, second = time
    new_hour = hour
    new_minute = minute - 1
    if new_minute < 0:
        new_minute = 59
        new_hour = hour - 1
        if new_hour < 0:
            new_hour = 23
    return (new_hour, new_minute, second)
