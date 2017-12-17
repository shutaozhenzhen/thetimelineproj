import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas

TEST_CASE = 1


class Canvas(TimelineCanvas):

    def __init__(self, parent):
        TimelineCanvas.__init__(self, parent)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_mousewheel)

    def _on_mousewheel(self, evt):
        if TEST_CASE == 1:
            self.ScrollHorizontallyOnMouseWheel(evt)
        elif TEST_CASE == 2:
            self.ZoomHorizontallyOnMouseWheel(evt)
        elif TEST_CASE == 3:
            self.ScrollVerticallyOnMouseWheel(evt)
        elif TEST_CASE == 4:
            self.ZoomVerticallyOnMouseWheel(evt)
        elif TEST_CASE == 5:
            self.SpecialScrollVerticallyOnMouseWheel(evt)
