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


from timelinelib.wxgui.components.maincanvas.inputhandler import InputHandler


# dragscroll timer interval in milliseconds
DRAGSCROLL_TIMER_MSINTERVAL = 30


class SelectBase(InputHandler):

    def __init__(self, timeline_canvas, x, y):
        InputHandler.__init__(self, timeline_canvas)
        self.timer_running = False
        self.start_pos = x, y

    def mouse_moved(self, x, y, alt_down=False):
        self.last_pos = x, y
        if not self.timer_running:
            self.timeline_canvas.start_dragscroll_timer(milliseconds=DRAGSCROLL_TIMER_MSINTERVAL)
            self.timer_running = True

    def left_mouse_up(self):
        self.timeline_canvas.stop_dragscroll_timer()
        self.timeline_canvas.RemoveRect()
        self.end_action()

    def dragscroll_timer_fired(self):
        self.timeline_canvas.DrawRect(self.start_pos, self.last_pos)
