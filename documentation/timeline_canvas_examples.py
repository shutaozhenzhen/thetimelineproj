def make_sure_timelinelib_can_be_imported():
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

def install_gettext_in_builtin_namespace():
    def _(message):
        return message
    import builtins
    if not "_" in builtins.__dict__:
        builtins.__dict__["_"] = _


make_sure_timelinelib_can_be_imported()
install_gettext_in_builtin_namespace()


import wx

from timelinelib.canvas import TimelineCanvas


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, size=(800, 400))
        self._create_canvas()
        self._display_example_timeline()

    def _create_canvas(self):
        self.canvas = TimelineCanvas(self)
        self.canvas.Bind(wx.EVT_MOUSEWHEEL, self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.Scroll(event.GetWheelRotation() / 1200.0)

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
