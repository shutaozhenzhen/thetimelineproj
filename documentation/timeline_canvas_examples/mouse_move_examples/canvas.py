import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas

TEST_CASE = 1


class Canvas(TimelineCanvas):

    def __init__(self, parent):
        self._parent = parent
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_MOTION, self._on_motion)

    def _on_motion(self, evt):
        self.DisplayBalloons(evt)
        self._parent.SetStatusText(self.GetTimelineInfoText(evt))
