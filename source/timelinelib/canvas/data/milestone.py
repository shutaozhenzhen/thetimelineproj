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


from timelinelib.canvas.data.event import Event


DEFAULT_COLOR = (255, 255, 128)

"""
 A milestone is a special case of a point event. It is normally rendered directly
 on the time scale. It is used to mark a milestone in a timeline.
"""


class Milestone(Event):

    def __init__(self, db, start_time, text):
        Event.__init__(self, db.time_type, start_time, start_time, text)
        self.set_default_color(DEFAULT_COLOR)

    def is_milestone(self):
        return True
