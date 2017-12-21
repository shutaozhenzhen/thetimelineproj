import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas
from timelinelib.canvas.data import TimePeriod


class CanvasPeriodSelect(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.InitDragPeriodSelect()

    def _on_left_down(self, evt):
        self.StartDragPeriodSelect(evt)

    def _on_motion(self, evt):
        self.DragPeriodSelect(evt)

    def _on_left_up(self, evt):
        start, end = self.StopDragPeriodSelect()
        print start, end
