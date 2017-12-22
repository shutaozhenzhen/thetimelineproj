import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas


class CanvasCombined(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.InitDragScroll(direction=wx.BOTH)
        self.InitDragSelect()
        self.InitZoomSelect()
        self.InitDragPeriodSelect()

    def _on_left_down(self, evt):
        if evt.ControlDown() and evt.ShiftDown():
            self.StartDragSelect(evt)
        elif evt.ControlDown():
            self.StartDragPeriodSelect(evt)
        elif evt.ShiftDown():
            self.StartZoomSelect(evt)
        else:
            self.StartDragScroll(evt)

    def _on_motion(self, evt):
        if evt.ControlDown() and evt.ShiftDown():
            self.DragSelect(evt)
        elif evt.ControlDown():
            self.DragPeriodSelect(evt)
        elif evt.ShiftDown():
            self.DragZoom(evt)
        else:
            self.DragScroll(evt)

    def _on_left_up(self, evt):
        if evt.ControlDown() and evt.ShiftDown():
            self.StopDragSelect()
        elif evt.ControlDown():
            self.StopDragPeriodSelect()
        elif evt.ShiftDown():
            self.StopDragZoom()
        else:
            self.StopDragScroll()
