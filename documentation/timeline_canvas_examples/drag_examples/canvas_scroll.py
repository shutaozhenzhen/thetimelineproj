import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas


class CanvasScroll(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.InitDragScroll(direction=wx.BOTH)

    def _on_left_down(self, evt):
        self.StartDragScroll(evt)

    def _on_motion(self, evt):
        self.DragScroll(evt)

    def _on_left_up(self, evt):
        self.StopDragScroll()
