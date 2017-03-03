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

"""Contains classes for debug monitoring and time measurement."""

import sys
import time


DEBUG_ENABLED = False


class Monitoring(object):
    """
    * Kepp track of the number of times the timeline has been redrawn.
    * Measure the time it takes to redraw a timeline.
    """
    def __init__(self):
        self.timeline_redraw_count = 0
        self.category_redraw_count = 0
        self.timer = Timer()

    def count_timeline_redraw(self):
        """Increment counter."""
        self.timeline_redraw_count += 1

    def count_category_redraw(self):
        """Increment counter."""
        self.category_redraw_count += 1

    def timer_start(self):
        """Start time measurment."""
        self.timer.start()

    def timer_end(self):
        """Stop time measurment."""
        self.timer.end()

    def timer_elapsed_ms(self):
        "return the elapsed time in milliseconds."
        return self.timer.elapsed_ms()


class Timer(object):
    """
    A general timer that can measure the elapsed time between
    a start and end time.
    """
    def __init__(self):
        # Taken from timeit.py (Python standard library)
        if sys.platform == "win32":
            # On Windows, the best timer is time.clock()
            self.default_timer = time.clock
        else:
            # On most other platforms the best timer is time.time()
            self.default_timer = time.time

    def start(self):
        """Start the timer."""
        self._start = self.default_timer()

    def end(self):
        """Stop the timer."""
        self._end = self.default_timer()

    def elapsed_ms(self):
        """Return the elapsed time i milliseconds."""
        return (self._end - self._start) * 1000
