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


import time

from timelinelib.wxgui.components.maincanvas.inputhandler import InputHandler


class ScrollByDragInputHandler(InputHandler):

    MAX_SPEED = 10000
    MAX_FRAME_RATE = 26.0

    def __init__(self, state, timeline_canvas, start_time, y):
        InputHandler.__init__(self, timeline_canvas)
        self._state = state
        self.start_slider_pos = self.timeline_canvas.GetDividerPosition()
        self.start_mouse_pos = y
        self.last_mouse_pos = y
        self.view_height = self.timeline_canvas.GetSize()[1]
        self.start_time = start_time
        self.last_clock_time = time.process_time()
        self.last_x = 0
        self.last_x_distance = 0
        self.last_y = 0
        self.last_y_distance = 0
        self.speed_px_per_sec = 0
        self.INERTIAL_SCROLLING_SPEED_THRESHOLD = 200

    def mouse_moved(self, cursor, keyboard):
        self.last_mouse_pos = cursor.y
        self._calculate_sped(cursor.x)
        self._scroll_timeline(cursor.x)
        percentage_distance = int(100 * (cursor.y - self.start_mouse_pos) / self.view_height)
        self.timeline_canvas.SetDividerPosition(self.start_slider_pos + percentage_distance)

    def left_mouse_up(self):
        if self.start_mouse_pos == self.last_mouse_pos:
            self.timeline_canvas.ClearSelectedEvents()
        self._state.change_to_no_op()
        self._state.edit_ends()
        if self.timeline_canvas.GetAppearance().get_use_inertial_scrolling():
            if self.speed_px_per_sec > self.INERTIAL_SCROLLING_SPEED_THRESHOLD:
                self._inertial_scrolling()

    def _calculate_sped(self, x):
        self.last_x_distance = x - self.last_x
        self.last_x = x
        current_clock_time = time.process_time()
        elapsed_clock_time = current_clock_time - self.last_clock_time
        if elapsed_clock_time == 0:
            self.speed_px_per_sec = self.MAX_SPEED
        else:
            self.speed_px_per_sec = min(
                self.MAX_SPEED,
                int(abs(self.last_x_distance / elapsed_clock_time))
            )
        self.last_clock_time = current_clock_time

    def _scroll_timeline(self, x):
        self.current_time = self.timeline_canvas.GetTimeAt(x)
        self.timeline_canvas.Navigate(lambda tp:
                                      tp.move_delta(self.start_time - self.current_time))

    def _inertial_scrolling(self):
        frame_time = self._calculate_frame_time()
        value_factor = self._calculate_scroll_factor()
        inertial_func = (0.20, 0.15, 0.10, 0.10, 0.10, 0.08, 0.06, 0.06, 0.05)
        self.timeline_canvas.UseFastDraw(True)
        next_frame_time = time.process_time()
        for value in inertial_func:
            self.timeline_canvas.Scroll(value * value_factor * 0.1)
            next_frame_time += frame_time
            sleep_time = next_frame_time - time.process_time()
            if sleep_time >= 0:
                time.sleep(sleep_time)
        self.timeline_canvas.UseFastDraw(False)

    def _calculate_frame_time(self):
        frames_per_second = self.MAX_FRAME_RATE * self.speed_px_per_sec / (100 + self.speed_px_per_sec)
        frame_time = 1.0 / frames_per_second
        return frame_time

    def _calculate_scroll_factor(self):
        if self.current_time > self.start_time:
            direction = 1
        else:
            direction = -1
        scroll_factor = (direction * self.speed_px_per_sec / self.INERTIAL_SCROLLING_SPEED_THRESHOLD)
        return scroll_factor
