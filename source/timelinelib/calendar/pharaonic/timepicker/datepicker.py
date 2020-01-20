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


from timelinelib.calendar.generic.timepicker.datepicker import DatePicker
from timelinelib.calendar.pharaonic.timepicker.datemodifier import PharaonicDateModifier
from timelinelib.calendar.pharaonic.dateformatter import PharaonicDateFormatter


class PharaonicDatePicker(DatePicker):

    def __init__(self, parent, name=None, on_change=None):
        DatePicker.__init__(self, parent, PharaonicDateModifier(), PharaonicDateFormatter(), on_change)
