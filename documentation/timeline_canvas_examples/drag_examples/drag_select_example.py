import wx

from canvas_select import CanvasSelect

from timelinelib.db import db_open


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, size=(800, 400))
        self._create_canvas()
        self._display_example_timeline()

    def _create_canvas(self):
        self.canvas = CanvasSelect(self)

    def _display_example_timeline(self):
        db_open(":tutorial:").display_in_canvas(self.canvas)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
