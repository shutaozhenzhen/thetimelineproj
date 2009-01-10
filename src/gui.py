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
                          wx.Point(0, 0), wx.Size(900, 400),
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
        create_new_event(self.timeline)
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
        # Initialize data members
        self.frame = parent

class DrawingArea(wx.Window):
    """
    Window on which the timeline is drawn.

    Double buffering is used to avoid flicker while drawing. This is
    accomplished by always drawing to a background buffer: bgbuf. The paint
    method of the control thus only draws the background buffer to the screen.

    This class has information about what part of a timeline to draw and makes
    sure that the timeline is redrawn whenever it is needed.
    """

    _marked_time = 0  # A time is marked when the left mouse button is pressed
    _mark_selection = False # Processing flag indicatingongoing selection

    def __init__(self, parent):
        wx.Window.__init__(self, parent, style=wx.NO_BORDER)
        # Definitions of colors and styles etc.
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetCursor(wx.CROSS_CURSOR)
        self.SetFocus()
        # Connect events
        wx.EVT_SIZE(self, self._on_size)
        wx.EVT_PAINT(self, self._on_paint)
        wx.EVT_LEFT_DOWN(self, self._on_left_down_event)
        wx.EVT_LEFT_UP(self, self._on_left_up_event)
        wx.EVT_MOTION(self, self._on_motion_event)
        wx.EVT_MOUSEWHEEL(self, self._on_mouse_wheel)
        wx.EVT_LEFT_DCLICK(self, self._on_left_dclick)
        wx.EVT_KEY_DOWN(self,self._on_key_down)
        # Initialize data members
        self.panel = parent
        self.bgbuf = None
        self.timeline = None
        self.time_period = None
        self.drawing_algorithm = drawing.get_algorithm()
        logging.debug("Init done in DrawingArea")

    def set_timeline(self, timeline):
        self.timeline = timeline
        self.time_period = timeline.preferred_period()
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

    def _on_key_down(self, evt):
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            ret  = wx.MessageBox('Are you sure to delete?', 'Question',
                                 wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT, self)
            if ret == wx.YES:
                self.timeline.delete_selected_events()
                self._draw_timeline()
        evt.Skip()

    def _on_mouse_wheel(self, evt):
        """Zooms the timeline when the mouse wheel is scrolled."""
        if evt.ControlDown():
            if (evt.m_wheelRotation < 0):
                self.time_period.zoom(-1)
            else:
                self.time_period.zoom(1)
        else:
            if (evt.m_wheelRotation < 0):
                self.time_period.move(1)
            else:
                self.time_period.move(-1)
        self._draw_timeline()

    def _on_left_down_event(self, evt):
        """The left mouse button has been pressed."""
        self.__set_new_marked_time(evt.m_x)
        self.__select_event(evt)
        evt.Skip()  # Needed to select the control

    def __set_new_marked_time(self, current_x):
        self._marked_time = self.drawing_algorithm.metrics.get_time(current_x)
        logging.debug("Marked time " + self._marked_time.isoformat('-'))

    def __select_event(self, evt):
        event = self.drawing_algorithm.event_at(evt.m_x, evt.m_y)
        # unselect all ?
        if not evt.m_controlDown:
            self.timeline.reset_selection()
        # An event is clicked
        if event != None:
            event.selected = not event.selected
        self._draw_timeline()

    def _on_left_up_event(self, evt):
        """The left mouse button has been released."""
        if self._mark_selection:
            self.__end_selection_and_create_event(evt.m_x)

    def __end_selection_and_create_event(self, current_x):
        self._mark_selection = False
        period_selection = self.__get_period_selection(current_x)
        start, end = period_selection
        create_new_event(self.timeline, start.isoformat('-'),
                         end.isoformat('-'))
        self._draw_timeline()

    def _on_motion_event(self, evt):
        """The mouse has been moved."""
        if not evt.Dragging:
            return
        if not evt.m_leftDown:
            return
        if evt.m_controlDown:
            self.__mark_selected_minor_strips(evt.m_x)
        else:
            self.__scoll_timeline(evt.m_x)

    def __scoll_timeline(self, current_x):
            current_time = self.drawing_algorithm.metrics.get_time(current_x)
            delta = current_time - self._marked_time
            self.time_period.start_time -= delta
            self.time_period.end_time   -= delta
            self._draw_timeline()

    def __mark_selected_minor_strips(self, current_x):
        self._mark_selection = True
        period_selection = self.__get_period_selection(current_x)
        self._draw_timeline(period_selection)

    def __get_period_selection(self, current_x):
        """Return a tuple containing the start and end time of a selection"""
        start = self._marked_time
        end   = self.drawing_algorithm.metrics.get_time(current_x)
        if start > end:
            start, end = end, start
        period_selection = self.drawing_algorithm.snap_selection((start,end))
        return period_selection

    def _on_left_dclick(self, evt):
        """The left mouse button has been doubleclicked"""
        logging.debug("Left doubleclick")
        event = self.drawing_algorithm.event_at(evt.m_x, evt.m_y)
        if event == None:
            self.__create_new_event()
        else:
            self.__edit_event(event)
        self._draw_timeline()

    def __create_new_event(self):
        """Open a dialog for creating a new event at the marked time"""
        create_new_event(self.timeline,
                         self._marked_time.isoformat('-'),
                         self._marked_time.isoformat('-'))

    def __edit_event(self, event):
        """Open a dialog for updating properties of a marked event"""
        dlg = EventDlg(None, -1, 'Edit Event', self.timeline, event=event)
        dlg.ShowModal()
        dlg.Destroy()

    def _draw_timeline(self, period_selection=None):
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
                current_events = self.timeline.get_events(self.time_period)
                self.drawing_algorithm.draw(memdc, self.time_period,
                                            current_events,
                                            period_selection)
            memdc.EndDrawing()
            self.Refresh()
        except Exception, e:
            self.bgbuf = None
            logging.fatal('Error in drawing', exc_info=e)


class EventDlg(wx.Dialog):
    """This dialog is used for creating and updating events"""
    _textctrl_start_time = None
    _textctrl_end_time = None
    _textctrl_name = None
    _timeline = None
    _cb_close_on_ok = None
    _editMode = False
    _event = None

    def __init__(self, parent, id, title, timeline, start=None, end=None, event=None):
        self._timeline = timeline
        wx.Dialog.__init__(self, parent, id, title, size=(250, 220))
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        wx.StaticBox(panel, -1, 'Event Properties', (5, 5), (230, 140))
        wx.StaticText(panel, -1, "Start:", (15,32), style=wx.ALIGN_LEFT)
        wx.StaticText(panel, -1, "End:"  , (15,62), style=wx.ALIGN_LEFT)
        wx.StaticText(panel, -1, "Name:" , (15,92), style=wx.ALIGN_LEFT)
        self._cb_close_on_ok = wx.CheckBox  (panel, -1, 'Close on OK', (15, 120 ))
        self._cb_close_on_ok.SetValue(True)
        if event != None:
            start = event.time_period.start_time.isoformat('-')
            end = event.time_period.end_time.isoformat('-')
            name = event.text
            self._updatemode = True
            self._event = event
        else:
            self._updatemode = False
            name = ''
        if start != None:
            start = start.split('.')[0]
        else:
            start = ''
        if end != None:
            end = end.split('.')[0]
        else:
            start = ''
        self._textctrl_start_time = wx.TextCtrl(panel, -1, start, (50, 30),(175,20))
        self._textctrl_end_time = wx.TextCtrl(panel, -1, end, (50, 60), (175,20))
        self._textctrl_name     = wx.TextCtrl(panel, -1, name, (50, 90), (175,20))
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
        if start == '':
            self._textctrl_start_time.SetFocus()
        elif end == '':
            self._textctrl_end_time.SetFocus()
        else:
            self._textctrl_name.SetFocus()

    def _on_close(self,e):
        self.Close()

    def _on_ok(self,e):
        try:
            start_time = self.__validate_start_time()
            end_time   = self.__validate_end_time()
            name       = self.__validate_name()
            if start_time > end_time:
                display_error_message("End must be > Start")
                set_focus_on_textctrl(self._textctrl_start_time)
                return
            if self._updatemode:
                self._event.update(start_time, end_time, name)
                self._timeline.save_events()
            else:
                event = Event(start_time, end_time, name)
                self._timeline.new_event(event)
            if self._cb_close_on_ok.GetValue():
                self.Close()
        except:
            pass

    def __validate_start_time(self):
        """Validate start time value from textbox"""
        try:
            start_time = todt(self._textctrl_start_time.GetValue())
        except:
            self.__display_dateformat_error()
            set_focus_on_textctrl(self._textctrl_start_time)
            raise
        return start_time

    def __validate_end_time(self):
        """Validate end time value from textbox"""
        try:
            end_time = todt(self._textctrl_end_time.GetValue())
        except:
            self.__display_dateformat_error()
            set_focus_on_textctrl(self._textctrl_end_time)
            raise
        return end_time

    def __validate_name(self):
        """Validate the name value from textbox"""
        try:
            name = self._textctrl_name.GetValue().strip()
            if len(name) == 0:
                raise
        except:
            display_error_message("Name: Can't be empty")
            set_focus_on_textctrl(self._textctrl_name)
            raise
        return name

    def __display_dateformat_error(self):
        """Display datetime fromat error message"""
        display_error_message('Date format must be "year-month-day"' +
                                ' or "year-month-day-hour:minue:second"')

def todt(datetime_string):
    """Convert a string to a datetime object"""
    args = datetime_string.strip().split('-')
    # Date only
    if len(args) == 3:
        return dt(int(args[0]),int(args[1]),int(args[2]))
    # Date and time
    elif len(args) == 4:
        time = args[3].split(':')
        if len(time) != 3:
            raise Excepetion("Unknown datetime format='%s'" % datetime_string)
        return dt(int(args[0]),int(args[1]),int(args[2]),
                  int(time[0]),int(time[1]),int(time[2]))
    # Unknown format
    else:
        raise Excepetion("Unknown datetime format='%s'" % datetime_string)

def create_new_event(timeline, start=None, end=None):
    """Create a new event"""
    dlg = EventDlg(None, -1, 'Create a new Event', timeline, start, end)
    dlg.ShowModal()
    dlg.Destroy()

def set_focus_on_textctrl(control):
    control.SetFocus()
    control.SelectAll()

def display_error_message(message):
    """Display an error message in a modal dialog box"""
    dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
    dial.ShowModal()
