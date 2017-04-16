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


class CalendarBase(object):

    def replace(self, year=None, month=None):
        raise NotImplementedError("replace not implemented.")

    def days_in_month(self):
        raise NotImplementedError("days_in_month not implemented.")

    def to_tuple(self):
        raise NotImplementedError("to_tuple not implemented.")

    def to_date_tuple(self):
        raise NotImplementedError("to_date_tuple not implemented.")

    def to_time_tuple(self):
        raise NotImplementedError("to_time_tuple not implemented.")

    def to_time(self):
        raise NotImplementedError("to_time not implemented.")

    def is_first_of_month(self):
        raise NotImplementedError("is_first_of_month not implemented.")

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.to_tuple() == other.to_tuple())

    def __repr__(self):
        raise NotImplementedError("__repr__ not implemented.")
