"""
Contains algorithms for drawing a timeline.
"""


from datetime import timedelta

import wx


class DrawingAlgorithm(object):
    """Base class for timeline drawing algorithms."""

    def draw(self, dc, time_period, events):
        """
        This is the interface.

        dc - used to do the actual drawing
        time_period - what period should of the timeline should be visible
        events - events inside time_period that should be drawn
        """
        pass


class SimpleDrawingAlgorithm(DrawingAlgorithm):

    def draw(self, dc, time_period, events):
        self.dc = dc
        self.time_period = time_period
        self.events = events
        self.metrics = Metrics(dc, time_period)
        self._draw_bg()
        self._calc_event_positions()
        self._draw_events()

    def _draw_bg(self):
        self.dc.SetPen(wx.Pen(wx.Color(0, 0, 0), 1, wx.SOLID))
        self.dc.DrawLine(0, self.metrics.half_height(),
                         self.metrics.width, self.metrics.half_height())
        self.dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_NORMAL))
        (tw, th) = self.dc.GetTextExtent(str(self.time_period.end_time))
        self.dc.DrawText(str(self.time_period.start_time), 5, self.metrics.half_height() - 15)
        self.dc.DrawText(str(self.time_period.end_time), self.metrics.width - tw - 5, self.metrics.half_height() - 15)

    def _calc_event_positions(self):
        self.eventspos = {}
        for event in self.events:
            start_time = event.time_period.start_time
            y = self.metrics.half_height()
            if event.is_period():
                y += 20
            else:
                y -= 20
            self.eventspos[event] = (self.metrics.get_x(start_time), y)

    def _draw_events(self):
        self.dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_NORMAL))
        for (event, pos) in self.eventspos.iteritems():
            (x, y) = pos
            (tw, th) = self.dc.GetTextExtent(event.text)
            self.dc.SetBrush(wx.Brush(wx.Color(200, 200, 0), wx.SOLID))
            if event.is_period():
                width = (self.metrics.get_x(event.time_period.end_time) - x)
            else:
                y -= th
                self.dc.SetPen(wx.Pen(wx.Color(0, 0, 0), 1, wx.SOLID))
                self.dc.DrawLine(x, self.metrics.half_height(), x, y)
                width = tw
                x -= tw / 2
            self.dc.DrawRectangle(x, y, width, th)
            self.dc.DrawText(event.text, x, y)


class Metrics(object):
    """Helper class that can calculate coordinates."""

    def __init__(self, dc, time_period):
        self.dc = dc
        self.width, self.height = dc.GetSizeTuple()
        self.time_period = time_period

    def get_x(self, time):
        # This is really ugly, but it works relatively well. If the / operator
        # were defined for timedelta this method could be written much simpler.
        pixperiod = self.time_period.delta() / self.width
        deltatotime = time - self.time_period.start_time
        tempdelta = timedelta()
        x = 0
        if tempdelta < deltatotime:
            # positive
            while tempdelta <= deltatotime:
                x += 1
                tempdelta += pixperiod
        else:
            # negative
            while tempdelta >= deltatotime:
                x -= 1
                tempdelta -= pixperiod
        return x

    def get_width(self, time_period):
        return self.get_x(time_period.end_time) - self.get_x(time_period.start_time)

    def half_height(self):
        return self.height / 2


def get_algorithm():
    """Factory method."""
    return SimpleDrawingAlgorithm()
