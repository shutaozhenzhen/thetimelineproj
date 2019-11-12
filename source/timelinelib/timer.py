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

"""
Contains the Timer class.

:doc:`Tests are found here <unit_timer>`.
"""

import sys
import time
import collections


class Timer:
    """
    A general timer that can measure the elapsed time between
    a start and end time.

    The timer function used, depends on os (as in timeit.py Python standard library)

    * On Windows, the best timer is time.clock()
    * On most other platforms the best timer is time.time()
    """
    def __init__(self, timer=None):
        self._start = None
        self._end = None
        self._default_timer = self._set_default_timer(timer)

    def start(self):
        """Start the timer."""
        self._start = self._default_timer()

    def end(self):
        """Stop the timer."""
        self._end = self._default_timer()

    @property
    def elapsed_ms(self):
        """Return the elapsed time in milliseconds between start and end."""
        return (self._end - self._start) * 1000

    @staticmethod
    def _set_default_timer(timer):
        if timer is not None:
            return timer
        elif sys.platform == "win32":
            return time.clock
        else:
            return time.time
