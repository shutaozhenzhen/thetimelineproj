import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas

TEST_CASE = 1


class Canvas(TimelineCanvas):

    def __init__(self, parent):
        self._parent = parent
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_MOTION, self._on_motion)

    def _on_left_down(self, evt):
        self.ToggleEventSelection(evt)

    def _on_motion(self, evt):
        self.SetCursorShape(evt)
