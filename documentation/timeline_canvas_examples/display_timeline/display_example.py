import timelineadaptor

import wx

from timelinelib.canvas import TimelineCanvas


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, size=(800, 400))
        self._create_canvas()
        self._display_example_timeline()

    def _create_canvas(self):
        self.canvas = TimelineCanvas(self)

    def _display_example_timeline(self):
        # The only way to populate the canvas at the moment is to use a
        # database object from Timeline and call its display_in_canvas method.
        from timelinelib.db import db_open
        db = db_open(":tutorial:")
        db.display_in_canvas(self.canvas)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
