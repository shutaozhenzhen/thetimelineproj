import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas
from timelinelib.canvas.data import TimePeriod


class CanvasZoom(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.InitZoomSelect()

    def _on_left_down(self, evt):
        self.StartZoomSelect(evt)

    def _on_motion(self, evt):
        self.DragZoom(evt)

    def _on_left_up(self, evt):
        self.StopDragZoom()
