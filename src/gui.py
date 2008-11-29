"""
GUI components.

The GUI components are mainly for interacting with the user and should not
contain much logic. For example, the `drawing' module is responsible for
drawing the timeline, but the `DrawingArea' class in this module provides the
GUI component on which it will draw.
"""


import logging

import wx

import data
import drawing


class MainFrame(wx.Frame):
    """
    The main frame of the application.

    Can be resized, maximized and minimized. The frame contains one panel.

    Holds an instance of a timeline that is currently being displayed.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "The Timeline Project",
                          wx.Point(0, 0), wx.Size(600, 400),
                          style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)
        # Build GUI
        self.main_panel = MainPanel(self)
        # Connect events
        wx.EVT_CLOSE(self, self._on_close)
        # Initialize data members
        self.timeline = None

    def open_timeline(self, input_files):
        if self.timeline:
            # TODO: Ask if save first or cancel
            pass
        self.timeline = data.get_timeline(input_files)
        if self.timeline:
            self.main_panel.drawing_area.set_timeline(self.timeline)

    def _on_close(self, event):
        logging.debug("Close event MainFrame")
        self.Destroy()


class MainPanel(wx.Panel):
    """
    Panel that covers the whole client area of MainFrame.

    At the moment, the panel only contains a single control: DrawingArea.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition,
                          size=wx.DefaultSize)
        # Build GUI
        self.drawing_area = DrawingArea(self)
        self.SetAutoLayout(True)
        self.globalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.globalSizer.Add(self.drawing_area, flag=wx.GROW, proportion=2)
        self.globalSizer.SetSizeHints(self)
        self.SetSizer(self.globalSizer)


class DrawingArea(wx.Window):
    """
    Window on which the timeline is drawn.

    Double buffering is used to avoid flicker while drawing. This is
    accomplished by always drawing to a background buffer: bgbuf. The paint
    method of the control thus only draws the background buffer to the screen.

    This class has information about what part of a timeline to draw and makes
    sure that the timeline is redrawn whenever it is needed.
    """

    def __init__(self, parent):
        wx.Window.__init__(self, parent, style=wx.NO_BORDER)
        # Definitions of colors and styles etc.
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetCursor(wx.CROSS_CURSOR)
        # Connect events
        wx.EVT_SIZE(self, self._on_size)
        wx.EVT_PAINT(self, self._on_paint)
        wx.EVT_MOUSEWHEEL(self, self._on_mouse_wheel)
        # Initialize data members
        self.bgbuf = None
        self.timeline = None
        self.time_period = None
        self.current_events = None
        self.drawing_algorithm = drawing.get_algorithm()
        logging.debug("Init done in DrawingArea")

    def set_timeline(self, timeline):
        self.timeline = timeline
        self.time_period = timeline.preferred_period()
        self.current_events = self.timeline.get_events(self.time_period)
        self._draw_timeline()

    def _on_size(self, event):
        """
        Called at the application start and when the frame is resized.

        Here we create a new background buffer with the new size and draw the
        timeline onto it.
        """
        logging.debug("Resize event in DrawingArea: %s", self.GetSizeTuple())
        width, height = self.GetSizeTuple()
        self.bgbuf = wx.EmptyBitmap(width, height)
        self._draw_timeline()

    def _on_paint(self, event):
        """
        Called at the application start, after resizing, or when the window
        becomes active.

        Here we just draw the background buffer onto the screen.
        """
        # Defining a dc is crucial. Even if it is not used.
        logging.debug("Paint event in DrawingArea")
        dc = wx.BufferedPaintDC(self)
        dc.BeginDrawing()
        if self.bgbuf:
            dc.DrawBitmap(self.bgbuf, 0, 0, True)
        dc.EndDrawing()

    def _on_mouse_wheel(self, evt):
        """Zooms the timeline when the mouse wheel is scrolled."""
        if (evt.m_wheelRotation < 0):
            self.time_period.zoom(-1)
        else:
            self.time_period.zoom(1)
        self.current_events = self.timeline.get_events(self.time_period)
        self._draw_timeline()

    def _draw_timeline(self):
        """
        Draws the timeline onto the background buffer.
        """
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.bgbuf)
        try:
            logging.debug('Draw timeline to bgbuf')
            memdc.BeginDrawing()
            memdc.SetBackground(wx.Brush(wx.WHITE, wx.SOLID))
            memdc.Clear()
            if self.timeline:
                self.drawing_algorithm.draw(memdc, self.time_period,
                                            self.current_events)
            memdc.EndDrawing()
            self.Refresh()
        except Exception, e:
            self.bgbuf = None
            logging.fatal('Error in drawing', exc_info=e)
