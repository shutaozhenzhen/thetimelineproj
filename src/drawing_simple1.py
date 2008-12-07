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


# Parameters that configure whitespace kinda
INNER_PADDING = 3
OUTER_PADDING = 5
THRESHOLD_PIX = 20
FOO = 10

STRIP_YEAR = 1
STRIP_MONTH = 2
STRIP_DAY = 3
STRIP_HOUR = 4
STRIP_MINUTE = 5

STRIP_HEADER = {
    STRIP_YEAR: "",
    STRIP_MONTH: "%Y",
    STRIP_DAY: "%B %Y",
    STRIP_HOUR: "%d %B %Y",
    STRIP_MINUTE: "%d %B %Y %H",
}

STRIP_LABEL = {
    STRIP_YEAR: "%Y",
    STRIP_MONTH: "%m",
    STRIP_DAY: "%d",
    STRIP_HOUR: "%H",
    STRIP_MINUTE: "%M",
}

STRIP_INC_FUNC = {
    STRIP_YEAR: (lambda x: x.replace(year=x.year+1)),
    STRIP_MONTH: (lambda x: x + timedelta(calendar.monthrange(x.year, x.month)[1])),
    STRIP_DAY: (lambda x: x + timedelta(1)),
    STRIP_HOUR: (lambda x: x + timedelta(0, 60*60)),
    STRIP_MINUTE: (lambda x: x + timedelta(0, 60)),
}

STRIP_START_FUNC = {
    STRIP_YEAR: (lambda x: datetime(x.year, 1, 1)),
    STRIP_MONTH: (lambda x: datetime(x.year, x.month, 1)),
    STRIP_DAY: (lambda x: datetime(x.year, x.month, x.day)),
    STRIP_HOUR: (lambda x: datetime(x.year, x.month, x.day, x.hour)),
    STRIP_MINUTE: (lambda x: datetime(x.year, x.month, x.day, x.hour, x.minute)),
}


class SimpleDrawingAlgorithm1(DrawingAlgorithm):

    def __init__(self):
        self.header_font = drawing.get_default_font(9, True)
        self.event_font = drawing.get_default_font(8)
        self.solid_pen = wx.Pen(wx.Color(0, 0, 0), 1, wx.SOLID)
        self.dashed_pen = wx.Pen(wx.Color(200, 200, 200), 1, wx.LONG_DASH)
        self.solid_brush = wx.Brush(wx.Color(0, 0, 0), wx.SOLID)

    def draw(self, dc, time_period, events):
        # Store data so we can use it in other functions
        self.dc = dc
        self.time_period = time_period
        self.metrics = Metrics(dc, time_period)
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
        self.rects = [] # List of tuples (event, rect)
        self.dc.SetFont(self.event_font)
        for event in events:
            tw, th = self.dc.GetTextExtent(event.text)
            ew = self.metrics.calc_width(event.time_period)
            if ew > THRESHOLD_PIX:
                # Tread as period
                rw = ew + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.calc_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height + OUTER_PADDING + FOO
                movedir = 1
            else:
                # Tread as event
                rw = tw + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.calc_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height - rh - OUTER_PADDING - FOO
                movedir = -1
            rect = wx.Rect(rx, ry, rw, rh)
            self._prevent_overlap(rect, movedir)
            self.rects.append((event, rect))
        # Remove outer padding
        for (event, rect) in self.rects:
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
        for (event, r) in self.rects:
            r_copy = wx.Rect(*r) # Because `Intersect` modifies rect
            intersection = r_copy.Intersect(rect)
            if not intersection.IsEmpty():
                return intersection.Height
        return 0

    def _calc_strips(self):
        """
        """
        self.strips = [] # List of tuples (time_period, label, major)
        t = self.time_period.start_time
        # START calc strip level
        if self.time_period.delta() > timedelta(365*2):
            self.strip_level = STRIP_YEAR
        elif self.time_period.delta() > timedelta(60):
            self.strip_level = STRIP_MONTH
        elif self.time_period.delta() > timedelta(2):
            self.strip_level = STRIP_DAY
        elif self.time_period.delta() > timedelta(0, 2):
            self.strip_level = STRIP_HOUR
        else:
            self.strip_level = STRIP_MINUTE
        logging.debug("Choosen strip = %s", self.strip_level)
        # END calc strip level
        start = STRIP_START_FUNC[self.strip_level](t)
        strip = STRIP_INC_FUNC[self.strip_level]
        while start < self.time_period.end_time:
            logging.debug("Strip loop, start = %s", start)
            next = strip(start)
            self.strips.append((TimePeriod(start, next),
                                self._strip_label(start), False))
            start = next

    def _strip_header(self, time_period):
        start_str = time_period.start_time.strftime(STRIP_HEADER[self.strip_level])
        end_str = time_period.end_time.strftime(STRIP_HEADER[self.strip_level])
        if start_str == end_str:
            return start_str
        return "%s - %s" % (start_str, end_str)

    def _strip_label(self, time):
        return time.strftime(STRIP_LABEL[self.strip_level])

    def _draw_bg(self):
        # Main divider line
        self.dc.DrawLine(0, self.metrics.half_height,
                         self.metrics.width, self.metrics.half_height)
        # Dividing lines
        self.dc.SetFont(self.event_font)
        for (p, label, major) in self.strips:
            x2 = self.metrics.calc_x(p.end_time)
            if major:
                self.dc.SetPen(self.solid_pen)
            else:
                self.dc.SetPen(self.dashed_pen)
            self.dc.DrawLine(x2, 0, x2, self.metrics.height)
            (tw, th) = self.dc.GetTextExtent(label)
            middle = self.metrics.calc_x(p.mean_time())
            middley = self.metrics.half_height
            self.dc.DrawText(label, middle - tw / 2, middley - th)
        # Lines to all events
        self.dc.SetPen(self.solid_pen)
        self.dc.SetBrush(self.solid_brush)
        for (event, rect) in self.rects:
            if rect.Y < self.metrics.half_height:
                x = rect.X + rect.Width / 2
                y = rect.Y + rect.Height / 2
                self.dc.DrawLine(x, y, x, self.metrics.half_height)
                self.dc.DrawCircle(x, self.metrics.half_height, 2)
        self.dc.SetFont(self.header_font)
        # Label
        strm = self._strip_header(self.time_period)
        (tw, th) = self.dc.GetTextExtent(strm)
        self.dc.DrawText(strm, self.metrics.half_width - tw / 2, INNER_PADDING)

    def _draw_events(self):
        self.dc.SetFont(self.event_font)
        self.dc.SetPen(self.solid_pen)
        for (event, rect) in self.rects:
            # Ensure that we can't draw outside rectangle
            self.dc.DestroyClippingRegion()
            self.dc.SetClippingRect(rect)
            self.dc.SetBrush(wx.Brush(wx.Color(200, 200, 0), wx.SOLID))
            self.dc.DrawRectangleRect(rect)
            self.dc.DrawText(event.text,
                             rect.X + INNER_PADDING,
                             rect.Y + INNER_PADDING)
