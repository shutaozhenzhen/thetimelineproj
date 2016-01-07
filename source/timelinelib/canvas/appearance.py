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


from timelinelib.utilities.observer import Observable


class Appearance(Observable):

    def __init__(self):
        Observable.__init__(self)
        self._build_property("legend_visible", True)
        self._build_property("balloons_visible", True)
        self._build_property("minor_strip_divider_line_colour", (200, 200, 200))
        self._build_property("major_strip_divider_line_colour", (200, 200, 200))
        self._build_property("now_line_colour", (200, 0, 0))
        self._build_property("draw_period_events_to_right", False)
        self._build_property("text_below_icon", False)

    def _build_property(self, name, initial_value):
        def getter():
            return getattr(self, "_%s" % name)
        def setter(new_value):
            old_value = getter()
            if new_value != old_value:
                setattr(self, "_%s" % name, new_value)
                self._notify()
        setattr(self, "get_%s" % name, getter)
        setattr(self, "set_%s" % name, setter)
        setattr(self, "_%s" % name, initial_value)
