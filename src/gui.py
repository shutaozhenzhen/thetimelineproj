"""
GUI components.

The GUI components are mainly for interacting with the user and should not
contain much logic. For example, the `drawing` module is responsible for
drawing the timeline, but the `DrawingArea` class in this module provides the
GUI component on which it will draw.
"""


import logging

from datetime import datetime as dt
import wx

from data import Event
import data_factory
import drawing

ID_NEW_EVENT   = 1


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
        # Create a menubar at the top of the user frame
        menuBar = wx.MenuBar()
        # Create a menu ...
        file_menu = wx.Menu()
        edit_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "E&xit\tAlt-F4", "Exit the program")
        edit_menu.Append(ID_NEW_EVENT, "&New Event", "Add a new event")
        # bind the menu event to an event handler, share QuitBtn event
        self.Bind(wx.EVT_MENU, self._on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self._on_new_event, id=ID_NEW_EVENT)
        # put the menu on the menubar
        menuBar.Append(file_menu, "&File")
        menuBar.Append(edit_menu, "&Edit")
        self.SetMenuBar(menuBar)
        # create a status bar at the bottom of the frame
        self.CreateStatusBar()
        # Connect events
        wx.EVT_CLOSE(self, self._on_close)
        # Initialize data members
        self.timeline = None
        self.input_files = None

    def refresh_timeline(self):
        self.timeline = data_factory.get_timeline(self.input_files)
        if self.timeline:
            self.main_panel.drawing_area.set_timeline(self.timeline)

    def open_timeline(self, input_files):
        if self.timeline:
            # TODO: Ask if save first or cancel
            pass
        self.input_files = input_files
        self.refresh_timeline()

    def _on_close(self, event):
        logging.debug("Close event MainFrame")
        self.Destroy()

    def _on_exit(self, evt):
        """Event handler for the Exit menu item"""
        logging.debug("Exit event MainFrame")
        self.Close()

    def _on_new_event(self, evt):
        """Event handler for the New Event menu item"""
        logging.debug("New Event event MainFrame")
        dlg = NewEventDlg(None, -1, 'Create a new Event', self.timeline)
        dlg.ShowModal()
        dlg.Destroy()
        self.refresh_timeline()


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


class NewEventDlg(wx.Dialog):
    """This dialog is used for registering new events"""

    _textctrl_start_time = None
    _textctrl_end_time = None
    _textctrl_name = None
    _timeline = None
    _cb = None

    def __init__(self, parent, id, title, timeline):
        self._timeline = timeline
        wx.Dialog.__init__(self, parent, id, title, size=(250, 220))
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        wx.StaticBox(panel, -1, 'Event Properties', (5, 5), (230, 140))
        wx.StaticText(panel, -1, "Start:", (15,32), style=wx.ALIGN_LEFT)
        wx.StaticText(panel, -1, "End:"  , (15,62), style=wx.ALIGN_LEFT)
        wx.StaticText(panel, -1, "Name:" , (15,92), style=wx.ALIGN_LEFT)
        self._cb = wx.CheckBox  (panel, -1, 'Close on OK', (15, 120 ))
        self._cb.SetValue(True)
        self._textctrl_start_time = wx.TextCtrl(panel, -1, '', (50, 30))
        self._textctrl_end_time = wx.TextCtrl(panel, -1, '', (50, 60))
        self._textctrl_name = wx.TextCtrl(panel, -1, '', (50, 90), (175,20))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, -1, 'Ok', size=(50, 25))
        wx.EVT_BUTTON(self, ok_button.GetId(), self._on_ok)
        close_button = wx.Button(self, -1, 'Close', size=(50, 25))
        wx.EVT_BUTTON(self, close_button.GetId(), self._on_close)
        hbox.Add(ok_button, 1)
        hbox.Add(close_button, 1, wx.LEFT, 5)
        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetDefaultItem(ok_button)
        self.SetSizer(vbox)
        self._textctrl_start_time.SetFocus()

    def _on_close(self,e):
        self.Close()

    def _on_ok(self,e):
        start = self._textctrl_start_time.GetValue().strip().split('-')
        end   = self._textctrl_end_time.GetValue().strip().split('-')
        name  = self._textctrl_name.GetValue().strip()

        if len(start) != 3:
            display_error_message('Date format must be "year-month-day"')
            set_focus_on_textctrl(self._textctrl_start_time)
            return

        if len(end) != 3:
            display_error_message('Date format must be "year-month-day"')
            set_focus_on_textctrl(self._textctrl_end_time)
            return

        if len(name) == 0:
            display_error_message("Name: Can't be empty")
            set_focus_on_textctrl(self._textctrl_name)
            return

        start_time = dt(int(start[0]),int(start[1]),int(start[2]))
        end_time   = dt(int(end[0]),int(end[1]),int(end[2]))

        if start_time > end_time:
            display_error_message("End must be > Start")
            set_focus_on_textctrl(self._textctrl_start_time)
            return

        event = Event(start_time,end_time, name)

        self._timeline.new_event(event)

        if self._cb.GetValue():
            self.Close()


def set_focus_on_textctrl(control):
    control.SetFocus()
    control.SelectAll()

def display_error_message(message):
    """Display an error message in a modal dialog box"""
    dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
    dial.ShowModal()
