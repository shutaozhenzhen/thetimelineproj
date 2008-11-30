"""
Contains algorithms for drawing a timeline.
"""

import logging
from datetime import timedelta

import wx

from drawing import DrawingAlgorithm
from drawing import Metrics


class SimpleDrawingAlgorithm2(DrawingAlgorithm):

    def draw(self, dc, time_period, events):
        logging.debug("Draw in SimpleDrawingAlgorithm2")
        self.dc = dc
        self.time_period = time_period
        self.events = events
        self.metrics = Metrics(dc, time_period)
        self._draw_bg()
        self._calc_event_positions()
        self._draw_events()
        del self.dc
        del self.metrics

    def _draw_bg(self):
        self.dc.SetPen(wx.Pen(wx.Color(255, 0, 0), 1, wx.SOLID))
        self.dc.DrawLine(0, self.metrics.half_height(),
                         self.metrics.width, self.metrics.half_height())
        self.dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_NORMAL))
        (tw, th) = self.dc.GetTextExtent(str(self.time_period.end_time))
        self.dc.DrawText(str(self.time_period.start_time), 5, self.metrics.half_height() - 15)
        self.dc.DrawText(str(self.time_period.end_time), self.metrics.width - tw - 5, self.metrics.half_height() - 15)

    def _calc_event_positions(self):
        logging.debug("_calc_event_positions")
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
        logging.debug("_draw_events")
        self.dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_NORMAL))
        for (event, pos) in self.eventspos.iteritems():
            (x, y) = pos
            (tw, th) = self.dc.GetTextExtent(event.text)
            self.dc.SetBrush(wx.Brush(wx.Color(200, 200, 200), wx.SOLID))
            if event.is_period():
                width = (self.metrics.get_x(event.time_period.end_time) - x)
            else:
                y -= th
                self.dc.SetPen(wx.Pen(wx.Color(200, 0, 0), 1, wx.SOLID))
                self.dc.DrawLine(x, self.metrics.half_height(), x, y)
                width = tw
                x -= tw / 2
            self.dc.DrawRectangle(x, y, width, th)
            self.dc.DrawText(event.text, x, y)