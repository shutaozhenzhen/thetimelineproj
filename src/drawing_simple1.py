"""
Implements a prototype algorithm for drawing a timeline.
"""


import logging
import calendar
from datetime import timedelta
from datetime import datetime

import wx

import drawing
from drawing import DrawingAlgorithm
from drawing import Metrics
from data import TimePeriod


OUTER_PADDING = 5      # Space between event boxes
INNER_PADDING = 3      # Space inside event box to text
THRESHOLD_PIX = 20     # Periods smaller than this are considered events
BASELINE_PADDING = 10  # Extra space to move events away from baseline


class Strip(object):

    def level(self, time_period):
        """Return if this strip type should be used for the given time period."""

    def label(self, time, long=False):
        """Return the label for this strip type at the given time."""

    def start(self, time):
        """Return the start time for this strip type and the given time."""

    def end(self, time):
        """Return the end time for this strip type and the given time."""
        return self.increment(self.start(time))

    def increment(self, time):
        """Increment the given time so that it points to the start of the next strip."""


class StripDecade(Strip):

    def decade_start_year(self, year):
        return (year / 10) * 10

    def level(self, time_period):
        return time_period.delta() > timedelta(365*15)

    def label(self, time, long=False):
        if long:
            return str(self.decade_start_year(time.year)) + "s"
        return ""

    def start(self, time):
        return datetime(self.decade_start_year(time.year), 1, 1)

    def increment(self, time):
        return time.replace(year=time.year+10)


class StripYear(Strip):

    def level(self, time_period):
        return time_period.delta() > timedelta(365*2)

    def label(self, time, long=False):
        return time.strftime("%Y")

    def start(self, time):
        return datetime(time.year, 1, 1)

    def increment(self, time):
        return time.replace(year=time.year+1)


class StripMonth(Strip):

    def level(self, time_period):
        return time_period.delta() > timedelta(40)

    def label(self, time, long=False):
        if long:
            return time.strftime("%b %Y")
        return time.strftime("%b")

    def start(self, time):
        return datetime(time.year, time.month, 1)

    def increment(self, time):
        return time + timedelta(calendar.monthrange(time.year, time.month)[1])


class StripDay(Strip):

    def level(self, time_period):
        return time_period.delta() > timedelta(2)

    def label(self, time, long=False):
        if long:
            return time.strftime("%b %d %Y")
        return str(time.day)

    def start(self, time):
        return datetime(time.year, time.month, time.day)

    def increment(self, time):
        return time + timedelta(1)


class StripHour(Strip):

    def level(self, time_period):
        return time_period.delta() > timedelta(0, 60)

    def label(self, time, long=False):
        if long:
            return time.strftime("%b %d %Y %h")
        return str(time.hour)

    def start(self, time):
        return datetime(time.year, time.month, time.day, time.hour)

    def increment(self, time):
        return time + timedelta(hours=1)


class SimpleDrawingAlgorithm1(DrawingAlgorithm):

    def __init__(self):
        self.header_font = drawing.get_default_font(12, True)
        self.event_font = drawing.get_default_font(8)
        self.solid_pen = wx.Pen(wx.Color(0, 0, 0), 1, wx.SOLID)
        self.dashed_pen = wx.Pen(wx.Color(200, 200, 200), 1, wx.LONG_DASH)
        self.solid_pen2 = wx.Pen(wx.Color(200, 200, 200), 1, wx.SOLID)
        self.solid_brush = wx.Brush(wx.Color(0, 0, 0), wx.SOLID)
        self.init_strips()

    def init_strips(self):
        self.strips = []
        self.strips.append(StripDecade())
        self.strips.append(StripYear())
        self.strips.append(StripMonth())
        self.strips.append(StripDay())
        self.strips.append(StripHour())

    def draw(self, dc, time_period, events):
        """
        Implement the drawing interface.

        The drawing is done in a number of steps: First positions of all events
        and strips are calculated and then they are drawn. Positions can also
        be used later to answer questions like what event is at position (x, y).
        """
        # Store data so we can use it in other functions
        self.dc = dc
        self.time_period = time_period
        self.metrics = Metrics(dc, time_period)
        # Data
        self.event_data = [] # List of tuples (event, rect)
        self.strip_data = [] # List of tuples (time_period)
        self.strip_sub_data = [] # List of tuples (time_period)
        # Calculate stuff later used for drawing
        self._calc_rects(events)
        self._calc_strips()
        # Perform the actual drawing
        self._draw_bg()
        self._draw_events()
        # Make sure to delete this one
        del self.dc

    def _calc_rects(self, events):
        """
        Calculate rectangles for all events.
        
        The rectangles define the areas in which the events can draw
        themselves.
        """
        self.dc.SetFont(self.event_font)
        for event in events:
            tw, th = self.dc.GetTextExtent(event.text)
            ew = self.metrics.calc_width(event.time_period)
            if ew > THRESHOLD_PIX:
                # Treat as period
                rw = ew + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.calc_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height + OUTER_PADDING + BASELINE_PADDING
                movedir = 1
            else:
                # Treat as event
                rw = tw + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.calc_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height - rh - OUTER_PADDING - BASELINE_PADDING
                movedir = -1
            rect = wx.Rect(rx, ry, rw, rh)
            self._prevent_overlap(rect, movedir)
            self.event_data.append((event, rect))
        # Remove outer padding
        for (event, rect) in self.event_data:
            rect.Deflate(OUTER_PADDING, OUTER_PADDING)

    def _prevent_overlap(self, rect, movedir):
        """
        Prevent rect from overlapping with any rectangle by moving it.
        """
        while True:
            h = self._intersection_height(rect)
            if h > 0:
                rect.Y += movedir * h
            else:
                break

    def _intersection_height(self, rect):
        """
        Calculate height of first intersection with rectangle.
        """
        for (event, r) in self.event_data:
            r_copy = wx.Rect(*r) # Because `Intersect` modifies rect
            intersection = r_copy.Intersect(rect)
            if not intersection.IsEmpty():
                return intersection.Height
        return 0

    def _calc_strips(self):
        prev_strip, strip = self._choose_strip()
        current_start = prev_strip.start(self.time_period.start_time)
        while current_start < self.time_period.end_time:
            next_start = prev_strip.increment(current_start)
            self.strip_data.append(TimePeriod(current_start, next_start))
            current_start = next_start
        current_start = strip.start(self.time_period.start_time)
        while current_start < self.time_period.end_time:
            next_start = strip.increment(current_start)
            self.strip_sub_data.append(TimePeriod(current_start, next_start))
            current_start = next_start

    def _choose_strip(self):
        prev_strip = None
        for strip in self.strips:
            if strip.level(self.time_period):
                if prev_strip == None:
                    return (strip, strip)
                return (prev_strip, strip)
            prev_strip = strip
        # Zoom level is high, resort to last one
        return (self.strips[-2], self.strips[-1])

    def _draw_bg(self):
        # Strips
        prev_strip, strip = self._choose_strip()
        self.dc.SetFont(self.event_font)
        for tp in self.strip_sub_data:
            # Strip line
            x2 = self.metrics.calc_x(tp.end_time)
            self.dc.SetPen(self.dashed_pen)
            self.dc.DrawLine(x2, 0, x2, self.metrics.height)
            # Strip label
            label = strip.label(tp.start_time)
            (tw, th) = self.dc.GetTextExtent(label)
            middle = self.metrics.calc_x(tp.mean_time())
            middley = self.metrics.half_height
            self.dc.DrawText(label, middle - tw / 2, middley - th)
        self.dc.SetFont(self.header_font)
        for tp in self.strip_data:
            # Strip line
            x2 = self.metrics.calc_x(tp.end_time)
            self.dc.SetPen(self.solid_pen2)
            self.dc.DrawLine(x2, 0, x2, self.metrics.height)
            # Section heading
            strm = prev_strip.label(tp.start_time, True)
            (tw, th) = self.dc.GetTextExtent(strm)
            x = self.metrics.calc_x(tp.mean_time()) - tw / 2
            if x - INNER_PADDING < 0:
                x = INNER_PADDING
                right = self.metrics.calc_x(tp.end_time)
                if x + tw + INNER_PADDING > right:
                    x = right - tw - INNER_PADDING
            elif x + tw / 2 + INNER_PADDING > self.metrics.width:
                x = self.metrics.width - tw - INNER_PADDING
                left = self.metrics.calc_x(tp.start_time)
                if x < left:
                    x = left + INNER_PADDING
            self.dc.DrawText(strm, x, INNER_PADDING)
        self.dc.SetPen(self.solid_pen)
        # Main divider line
        self.dc.DrawLine(0, self.metrics.half_height,
                         self.metrics.width, self.metrics.half_height)
        # Lines to all events
        self.dc.SetBrush(self.solid_brush)
        for (event, rect) in self.event_data:
            if rect.Y < self.metrics.half_height:
                x = rect.X + rect.Width / 2
                y = rect.Y + rect.Height / 2
                self.dc.DrawLine(x, y, x, self.metrics.half_height)
                self.dc.DrawCircle(x, self.metrics.half_height, 2)

    def _draw_events(self):
        self.dc.SetFont(self.event_font)
        self.dc.SetPen(self.solid_pen)
        for (event, rect) in self.event_data:
            # Ensure that we can't draw outside rectangle
            self.dc.DestroyClippingRegion()
            self.dc.SetClippingRect(rect)
            self.dc.SetBrush(wx.Brush(wx.Color(200, 200, 0), wx.SOLID))
            self.dc.DrawRectangleRect(rect)
            self.dc.DrawText(event.text,
                             rect.X + INNER_PADDING,
                             rect.Y + INNER_PADDING)
