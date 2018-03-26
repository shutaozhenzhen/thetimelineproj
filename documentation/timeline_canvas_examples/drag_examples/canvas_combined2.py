import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas
from timelinelib.wxgui.keyboard import Keyboard


class CanvasCombined2(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.InitDrag(scroll=self.BOTH,
                      zoom=Keyboard.SHIFT,
                      period_select=Keyboard.CTRL,
                      event_select=Keyboard.SHIFT | Keyboard.CTRL)

    def _on_left_down(self, evt):
        self.CallDragMethod(self.START, evt)

    def _on_motion(self, evt):
        self.CallDragMethod(self.DRAG, evt)

    def _on_left_up(self, evt):
        self.CallDragMethod(self.STOP, evt)
