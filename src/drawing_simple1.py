"""
Implements a prototype algorithm for drawing a timeline.
"""


import logging

import wx

from drawing import DrawingAlgorithm
from drawing import Metrics


INNER_PADDING = 3
OUTER_PADDING = 5
THRESHOLD_PIX = 20


class SimpleDrawingAlgorithm1(DrawingAlgorithm):

    def __init__(self):
        self.event_font = wx.Font(8, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL)

    def draw(self, dc, time_period, events):
        # Store data so that it can be reused in functions
        self.dc = dc
        self.time_period = time_period
        self.metrics = Metrics(dc, time_period)
        # Calc stuff
        self.data = self._calc_data(events)
        # Perform drawing
        self._draw_bg()
        self._draw_events()
        # Make sure to delete this
        del self.dc

    def _calc_data(self, events):
        """
        Calculate rectangles for all events.
        
        The rectangles define the areas in which the events can draw themselves.
        """
        data = [] # A list of tuples (event, rect)
        def overlap(r):
            """Calculate first intersection."""
            for (event, rect) in data:
                temp = wx.Rect(*r)
                intersection = temp.Intersect(rect)
                if not intersection.IsEmpty():
                    return intersection
            return None
        self.dc.SetFont(self.event_font)
        for event in events:
            (tw, th) = self.dc.GetTextExtent(event.text)
            ew = self.metrics.get_width(event.time_period)
            logging.debug("th = %s", th)
            if ew > THRESHOLD_PIX:
                # Tread as period
                rw = ew + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.get_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height() + OUTER_PADDING
                movedir = 1
            else:
                # Tread as event
                rw = tw + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rh = th + 2 * INNER_PADDING + 2 * OUTER_PADDING
                rx = self.metrics.get_x(event.mean_time()) - rw / 2
                ry = self.metrics.half_height() - rh - OUTER_PADDING
                movedir = -1
            rect = wx.Rect(rx, ry, rw, rh)
            # Move rect until there is no overlap
            while True:
                o = overlap(rect)
                if not o:
                    break
                rect.OffsetXY(0, movedir * o.Height)
            data.append((event, rect))
        # Remove outer padding
        for (event, rect) in data:
            logging.debug("Before deflate, %s", rect)
            rect.Deflate(OUTER_PADDING, OUTER_PADDING)
            logging.debug("After deflate, %s", rect)
            pass
        return data

    def _draw_bg(self):
        self.dc.SetPen(wx.Pen(wx.Color(0, 0, 0), 1, wx.SOLID))
        self.dc.DrawLine(0, self.metrics.half_height(),
                         self.metrics.width, self.metrics.half_height())
        self.dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_NORMAL))
        (tw, th) = self.dc.GetTextExtent(str(self.time_period.end_time))
        self.dc.DrawText(str(self.time_period.start_time), 5, self.metrics.half_height() - 15)
        self.dc.DrawText(str(self.time_period.end_time), self.metrics.width - tw - 5, self.metrics.half_height() - 15)

    def _draw_events(self):
        for (event, rect) in self.data:
            self.dc.SetBrush(wx.Brush(wx.Color(200, 200, 0), wx.SOLID))
            # Ensure that we can't draw outside rectangle
            self.dc.DestroyClippingRegion()
            self.dc.SetClippingRect(rect)
            self.dc.DrawRectangleRect(rect)
            self.dc.SetFont(self.event_font)
            self.dc.DrawText(event.text,
                             rect.X + INNER_PADDING,
                             rect.Y + INNER_PADDING)
