"""
GUI components.

The GUI components are mainly for interacting with the user and should not
contain much logic. For example, the drawing algorithm is responsible for
drawing the timeline, but the `DrawingArea` class in this module provides the
GUI component on which it will draw.
"""


import logging
import os.path
from datetime import datetime as dt

import wx
import wx.lib.colourselect as colourselect

from data import Event
from data import Category
import data
import drawing


ID_NEW_EVENT = 1
ID_CATEGORIES = 2
BORDER = 5


class MainFrame(wx.Frame):
    """
    The main frame of the application.

    Can be resized, maximized and minimized. The frame contains one panel.

    Holds an instance of a timeline that is currently being displayed.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, size=(900, 400),
                          style=wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE)
        self.__set_initial_values_to_member_variables()
        self.__create_gui()
        self._enable_disable_menus()
        self.Bind(wx.EVT_CLOSE, self._window_is_closing)

    def display_timeline(self, input_file):
        """Read timeline info from the given input file and display it."""
        try:
            self.timeline = data.get_timeline(input_file)
        except Exception, e:
            display_error_message("Unable to open timeline '%s'.\n\n%s" %
                                  (input_file, e))
        else:
            self.SetTitle("%s (%s)" % (self.title_base, input_file))
            self.main_panel.drawing_area.set_timeline(self.timeline)
        self._enable_disable_menus()

    def _create_new_timeline(self):
        """
        Create a new empty timeline.

        The user is asked to enter the filename of the new timeline to be
        created.

        If the new filename entered, should already exist, the existing
        timeline is opened. The user will be informed about this situation.
        """
        dialog = wx.FileDialog(self, message="Create Timeline",
                               wildcard=self.wildcard, style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            # If no extension, add default
            has_valid_extension = False
            for extension in self.extensions:
                if path.endswith(extension):
                    has_valid_extension = True
                    break
            if not has_valid_extension:
                path += self.default_extension
            if os.path.exists(path):
                wx.MessageBox("The specified timeline already exists.\n\n"
                              "Opening instead of creating new.", "Information",
                              wx.OK|wx.ICON_INFORMATION, self)
            self.display_timeline(path)
        dialog.Destroy()

    def _open_existing_timeline(self):
        """
        Open a new timeline.

        The user is asked to enter the filename of the timeline to be opened.
        """
        dialog = wx.FileDialog(self, message="Open Timeline",
                               wildcard=self.wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.display_timeline(dialog.GetPath())
        dialog.Destroy()

    def _enable_disable_menus(self):
        """
        Enable or disable menu items depending on the state of the application.
        """
        timeline_menu_index = 1
        timeline_menu = self.GetMenuBar().GetMenu(timeline_menu_index)
        if self.timeline == None:
            timeline_menu.Enable(ID_NEW_EVENT , False)
            timeline_menu.Enable(ID_CATEGORIES, False)
        else:
            timeline_menu.Enable(ID_NEW_EVENT , True)
            timeline_menu.Enable(ID_CATEGORIES, True)

    def _mnu_file_new_clicked(self, event):
        """Event handler used when the user wants to create a new timeline."""
        self._create_new_timeline()

    def _mnu_file_open_clicked(self, event):
        """Event handler used when the user wants to open a new timeline."""
        self._open_existing_timeline()

    def _window_is_closing(self, event):
        self.Destroy()

    def _mnu_file_exit_clicked(self, evt):
        """Event handler for the Exit menu item"""
        self.Close()

    def _mnu_timeline_create_event_clicked(self, evt):
        """Event handler for the New Event menu item"""
        if create_new_event(self.timeline) == wx.ID_OK:
            self.main_panel.drawing_area.draw_timeline()

    def _mnu_timeline_edit_categories_clicked(self, evt):
        """Event handler for the Edit Categories menu item"""
        if edit_categories(self.timeline) == wx.ID_OK:
            self.main_panel.drawing_area.draw_timeline()

    def __set_initial_values_to_member_variables(self):
        """
        Instance variables usage:

        timeline            The timeline currently handled by the application
        title_base          The prefix of the title displayed in the title bar
        extensions          Valid extensions for files containing timeline info
        default_extension   The default extension used in FileDialog
        wildcard            The wildcard used in FileDialog
        """
        self.timeline = None
        self.title_base = "The Timeline Project"
        self.extensions = [".timeline"]
        self.default_extension = self.extensions[0]
        self.wildcard = "Timeline file (%s)|%s" % (
            ", ".join(["*" + e for e in self.extensions]),
            ";".join(["*" + e for e in self.extensions]))

    def __create_gui(self):
        self.main_panel = MainPanel(self)
        self.SetTitle(self.title_base)
        self.CreateStatusBar()
        self.__create_menu()

    def __create_menu(self):
        # Main menus
        file_mnu = wx.Menu()
        timeline_mnu = wx.Menu()
        # Submenus
        file_mnu.Append(wx.ID_NEW, "&New...\tCtrl+N", "Create a new timeline")
        file_mnu.Append(wx.ID_OPEN, "&Open...\tCtrl+O", "Open an existing timeline")
        file_mnu.AppendSeparator()
        file_mnu.Append(wx.ID_EXIT, "E&xit\tAlt-F4", "Exit the program")
        timeline_mnu.Append(ID_NEW_EVENT, "&Create Event", "Create a new event")
        timeline_mnu.Append(ID_CATEGORIES, "Edit &Categories", "Edit categories")
        # Bind event handlers to menus
        self.Bind(wx.EVT_MENU, self._mnu_file_new_clicked, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self._mnu_file_open_clicked, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._mnu_file_exit_clicked, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self._mnu_timeline_create_event_clicked, id=ID_NEW_EVENT)
        self.Bind(wx.EVT_MENU, self._mnu_timeline_edit_categories_clicked, id=ID_CATEGORIES)
        # The Menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(file_mnu, "&File")
        menuBar.Append(timeline_mnu, "&Timeline")
        self.SetMenuBar(menuBar)


class MainPanel(wx.Panel):
    """
    Panel that covers the whole client area of MainFrame.

    At the moment, the panel only contains a single control: DrawingArea.
    """

    def __init__(self, parent):
        """Create the Main Panel."""
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition,
                          size=wx.DefaultSize)
        self.frame = parent
        self.__create_gui()

    def __create_gui(self):
        """Create the controls of the Main Panel."""
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

    Scrolling and zooming of the timeline is implemented in this class. This is
    done whenever the mouse wheel is scrolled (_mouse_wheel_has_scrolled).
    Moving also takes place when the mouse is dragged while pressing the left
    mouse key (_mouse_has_moved).

    Selection of a period on the timeline (period = any number of minor strips)
    is also implemented in this class. A selection is done in the following
    way: Press and hold down the Control key on the keyboard, move the mouse to
    the first minor strip to be selected and then press and hold down the left
    mouse key. Now, while moving the mouse over the timeline, the minor strips
    will be selected.

    What happens is that when the left mouse button is pressed
    (_left_mouse_button_pressed) the variable self._current_time is set to the
    time on the timeline where the mouse is. This is the anchor point for the
    selection. When the mouse is moved (_mouse_has_moved) and left mouse button
    is pressed and the Control key is held down the method
    self.__mark_selected_minor_strips(evt.m_x) is called. This method marks all
    minor strips between the anchor point and the current point (evt.m_x).
    When the mouse button is released the selection ends.
    """

    def __init__(self, parent):
        wx.Window.__init__(self, parent, style=wx.NO_BORDER)
        self.__set_initial_values_to_member_variables()
        self.__set_colors_and_styles()
        self.__bind_events_to_handlers();
        logging.debug("Init done in DrawingArea")

    def set_timeline(self, timeline):
        self.timeline = timeline
        self.time_period = timeline.get_preferred_period()
        self.draw_timeline()
        self.Enable()
        self.SetFocus()

    def draw_timeline(self, period_selection=None):
        """Draws the timeline onto the background buffer."""
        logging.debug('Draw timeline to bgbuf')
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.bgbuf)
        try:
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
        except Exception, ex:
            self.bgbuf = None
            logging.fatal('Error in drawing', exc_info=ex)

    def __set_initial_values_to_member_variables(self):
        """
        Instance variables usage:

        _current_time       This variable is set to the time on the timeline
                            where the mouse button is clicked when the left
                            mouse button is used
        _mark_selection     Processing flag indicating ongoing selection of a
                            time period
        timeline            The timeline currently handled by the application
        time_period         The part of the timeline currently displayed in the
                            drawing area
        drawing_algorithm   The algorithm used to draw the timeline
        bgbuf               The bitmap to which the drawing methods draw the
                            timeline. When the EVT_PAINT occurs this bitmap
                            is painted on the screen. This is a buffer drawing
                            approach for avoiding screen flicker.
        is_scrolling        True when scrolling with the mouse takes place.
                            It is set True in mouse_has_moved and set False
                            in left_mouse_button_released.
        is_selecting        True when selecting with the mouse takes place
                            It is set True in mouse_has_moved and set False
                            in left_mouse_button_released.
        """
        self._current_time = None
        self._mark_selection = False
        self.bgbuf = None
        self.timeline = None
        self.time_period = None
        self.drawing_algorithm = drawing.get_algorithm()
        self.is_scrolling = False
        self.is_selecting = False

    def __set_colors_and_styles(self):
        """Define the look and feel of the drawing area."""
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetCursor(wx.CROSS_CURSOR)
        self.Disable()

    def __bind_events_to_handlers(self):
        self.Bind(wx.EVT_SIZE, self._window_resized)
        self.Bind(wx.EVT_PAINT, self._window_needs_repaint)
        self.Bind(wx.EVT_LEFT_DOWN, self._left_mouse_button_pressed)
        self.Bind(wx.EVT_LEFT_DCLICK, self._left_mouse_button_doubleclicked)
        self.Bind(wx.EVT_LEFT_UP, self._left_mouse_button_released)
        self.Bind(wx.EVT_MOTION, self._mouse_has_moved)
        self.Bind(wx.EVT_MOUSEWHEEL, self._mouse_wheel_has_scrolled)
        self.Bind(wx.EVT_KEY_DOWN, self._keyboard_key_pressed)

    def _window_resized(self, event):
        """
        Event handler used when the window has been resized.

        Called at the application start and when the frame is resized.

        Here we create a new background buffer with the new size and draw the
        timeline onto it.
        """
        logging.debug("Resize event in DrawingArea: %s", self.GetSizeTuple())
        width, height = self.GetSizeTuple()
        self.bgbuf = wx.EmptyBitmap(width, height)
        self.draw_timeline()

    def _window_needs_repaint(self, event):
        """
        Event handler used when the window needs repainting.

        Called at the application start, after resizing, or when the window
        becomes active.

        Here we just draw the background buffer onto the screen.

        Defining a dc is crucial. Even if it is not used.
        """
        logging.debug("Paint event in DrawingArea")
        dc = wx.BufferedPaintDC(self)
        dc.BeginDrawing()
        dc.DrawBitmap(self.bgbuf, 0, 0, True)
        dc.EndDrawing()

    def _left_mouse_button_pressed(self, evt):
        """
        Event handler used when the left mouse button has been pressed.

        This event establishes a new current time on the timeline.

        If the mouse hits an event that event will be selected.
        """
        logging.debug("Left mouse pressed event in DrawingArea")
        self.__set_new_current_time(evt.m_x)
        self.__toggle_event_selection(evt.m_x, evt.m_y, evt.m_controlDown)
        evt.Skip()

    def _left_mouse_button_doubleclicked(self, evt):
        """
        Event handler used when the left mouse button has been double clicked.

        If the mouse hits an event, a dialog opens for editing this event.
        Otherwise a dialog for creating a new event is opened.
        """
        logging.debug("Left Mouse doubleclicked event in DrawingArea")
        event = self.drawing_algorithm.event_at(evt.m_x, evt.m_y)
        if event:
            edit_event(self.timeline, event)
        else:
            create_new_event(self.timeline,
                             self._current_time.isoformat('-'),
                             self._current_time.isoformat('-'))
        self.draw_timeline()

    def _left_mouse_button_released(self, evt):
        """
        Event handler used when the left mouse button has been released.

        If there is an ongoing selection-marking, the dialog for creating an
        event will be opened, and the selection-marking will be ended.
        """
        logging.debug("Left mouse released event in DrawingArea")
        if self.is_selecting:
            self.__end_selection_and_create_event(evt.m_x)
        self.is_selecting = False
        self.is_scrolling = False

    def _mouse_has_moved(self, evt):
        """
        Event handler used when the mouse has been moved.

        If the mouse is over an event, the name of that event will be printed
        in the status bar.

        If the left mouse key is down one of two things happens depending on if
        the Control key is down or not. If it is down a selection-marking takes
        place and the minor strips passed by the mouse will be selected.  If
        the Control key is up the timeline will scroll.
        """
        logging.debug("Mouse move event in DrawingArea")
        if evt.Dragging:
            self.__display_eventname_in_statusbar(evt.m_x, evt.m_y)
        if evt.m_leftDown:
            if self.is_scrolling:
                self.__scroll(evt.m_x)
            elif self.is_selecting:
                self.__mark_selected_minor_strips(evt.m_x)
            else:
                if evt.m_controlDown:
                    self.__mark_selected_minor_strips(evt.m_x)
                    self.is_selecting = True
                else:
                    self.__scroll(evt.m_x)
                    self.is_scrolling = True

    def __scroll(self, xpixelpos):
        if self._current_time:
            delta = (self.drawing_algorithm.metrics.get_time(xpixelpos) -
                        self._current_time)
            self.__scroll_timeline(delta)

    def _mouse_wheel_has_scrolled(self, evt):
        """
        Event handler used when the mouse wheel is rotated.

        If the Control key is pressed at the same time as the mouse wheel is
        scrolled the timeline will be zoomed, otherwise it will be scrolled.
        """
        logging.debug("Mouse wheel event in DrawingArea")
        direction = step_function(evt.m_wheelRotation)
        if evt.ControlDown():
            self.__zoom_timeline(direction)
        else:
            delta = data.mult_timedelta(self.time_period.delta(),
                                        direction / 10.0)
            self.__scroll_timeline(delta)

    def _keyboard_key_pressed(self, evt):
        """
        Event handler used when a keyboard key has been pressed.

        The following keys are handled:
        Key         Action
        --------    ------------------------------------
        Delete      Delete any selected event(s)
        """
        logging.debug("Key down event in DrawingArea")
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            self.__delete_selected_events()
        evt.Skip()

    def __set_new_current_time(self, current_x):
        self._current_time = self.drawing_algorithm.metrics.get_time(current_x)
        logging.debug("Marked time " + self._current_time.isoformat('-'))

    def __toggle_event_selection(self, xpixelpos, ypixelpos, control_down):
        """
        If the given position is within the boundaries of an event that event
        will be selected or unselected depending on the current selection
        state of the event. If the Control key is down all other events
        selection state are preserved. This means that previously selected
        events will stay selected. If the Control keys is not down all other
        events will be unselected.

        If the given position isn't within an event all selected events will
        be unselected.
        """
        event = self.drawing_algorithm.event_at(xpixelpos, ypixelpos)
        if event:
            selected = event.selected
            if not control_down:
                self.timeline.reset_selection()
            event.selected = not selected
        else:
            self.timeline.reset_selection()
        self.draw_timeline()

    def __end_selection_and_create_event(self, current_x):
        self._mark_selection = False
        period_selection = self.__get_period_selection(current_x)
        start, end = period_selection
        create_new_event(self.timeline, start.isoformat('-'),
                         end.isoformat('-'))
        self.draw_timeline()

    def __display_eventname_in_statusbar(self, xpixelpos, ypixelpos):
        """
        If the given position is within the boundaries of an event, the name of
        that event will be displayed in the status bar, otherwise the status
        bar text will be removed.
        """
        event = self.drawing_algorithm.event_at(xpixelpos, ypixelpos)
        if event != None:
            self.__display_text_in_statusbar(event.text)
        else:
            self.__reset_text_in_statusbar()

    def __mark_selected_minor_strips(self, current_x):
        """Selection-marking starts or continues."""
        self._mark_selection = True
        period_selection = self.__get_period_selection(current_x)
        self.draw_timeline(period_selection)

    def __scroll_timeline(self, delta):
        self.time_period.move_delta(-delta)
        self.timeline.set_preferred_period(self.time_period)
        self.draw_timeline()

    def __zoom_timeline(self, direction=0):
        self.time_period.zoom(direction)
        self.timeline.set_preferred_period(self.time_period)
        self.draw_timeline()

    def __delete_selected_events(self):
        """After acknowledge from the user, delete all selected events."""
        ok_to_delete  = wx.MessageBox('Are you sure to delete?', 'Question',
                                      wx.YES_NO|wx.CENTRE|wx.NO_DEFAULT,
                                      self) == wx.YES
        if ok_to_delete:
            self.timeline.delete_selected_events()
            self.draw_timeline()

    def __get_period_selection(self, current_x):
        """Return a tuple containing the start and end time of a selection."""
        start = self._current_time
        end   = self.drawing_algorithm.metrics.get_time(current_x)
        if start > end:
            start, end = end, start
        period_selection = self.drawing_algorithm.snap_selection((start,end))
        return period_selection

    def __display_text_in_statusbar(self, text):
        wx.GetTopLevelParent(self).SetStatusText(text)

    def __reset_text_in_statusbar(self):
        wx.GetTopLevelParent(self).SetStatusText('')


class EventEditor(wx.Dialog):
    """This dialog is used for creating and updating events."""

    def __init__(self, parent, id, title, timeline, start=None, end=None,
                 event=None):
        """
        Create a event editor dialog.

        The dialog can be used both for creating new events and for updating
        old ones.

        The 'event' argument is optional. If it is given the dialog is used
        to update this event and the textboxes are filled with data from
        the event and the arguments 'start' and 'end' are ignored.

        If the 'event' argument isn't given the dialog is used to create a
        new event, and the textboxes for start and end time are initially
        filled with data from the arguments 'start' and 'end' if they are
        given.
        """
        wx.Dialog.__init__(self, parent, id, title)
        self._timeline = timeline
        self._event = event
        self.__create_gui()
        self.__fill_controls_with_data(start, end)
        self.__set_initial_focus()

    def __create_gui(self):
        """Create the controls of the dialog."""
        grid = wx.FlexGridSizer(4, 2, BORDER, BORDER)
        CTRL_MIN_WIDTH = 160
        self._txt_start_time = wx.TextCtrl(self, wx.ID_ANY,
                                           size=(CTRL_MIN_WIDTH, -1))
        self._txt_end_time = wx.TextCtrl(self, wx.ID_ANY,
                                         size=(CTRL_MIN_WIDTH, -1))
        self._txt_name = wx.TextCtrl(self, wx.ID_ANY,
                                     size=(CTRL_MIN_WIDTH, -1))
        self._lst_category = wx.Choice(self, wx.ID_ANY,
                                       size=(CTRL_MIN_WIDTH, -1))
        grid.AddMany([
            (wx.StaticText(self, wx.ID_ANY, "Start:"), 0,
                           wx.ALIGN_CENTER_VERTICAL), (self._txt_start_time),
            (wx.StaticText(self, wx.ID_ANY, "End:"), 0,
                           wx.ALIGN_CENTER_VERTICAL), (self._txt_end_time),
            (wx.StaticText(self, wx.ID_ANY, "Name:"), 0,
                           wx.ALIGN_CENTER_VERTICAL), (self._txt_name),
            (wx.StaticText(self, wx.ID_ANY, "Category:"), 0,
                           wx.ALIGN_CENTER_VERTICAL), (self._lst_category),
        ])
        # The Group box
        groupbox = wx.StaticBox(self, wx.ID_ANY, "Event Properties")
        groupbox_sizer = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        groupbox_sizer.Add(grid, 0, wx.ALL, BORDER)
        # The checkbox
        self._cbx_close_on_ok = wx.CheckBox(self, wx.ID_ANY, "Close on OK")
        # Add controls and buttons do the dialog
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(groupbox_sizer, 1, wx.EXPAND|wx.ALL, BORDER)
        main_box.Add(self._cbx_close_on_ok, 0, wx.EXPAND|wx.ALL, BORDER)
        main_box.Add(self.__create_button_box(), 0, wx.EXPAND|wx.ALL, BORDER)
        self.SetSizerAndFit(main_box)

    def __fill_controls_with_data(self, start=None, end=None):
        """Initially fill the controls in the dialog with data."""
        # Text fields
        if self._event != None:
            start = self._event.time_period.start_time.isoformat('-')
            end = self._event.time_period.end_time.isoformat('-')
            name = self._event.text
            category = self._event.category
            self._updatemode = True
        else:
            self._updatemode = False
            name = ''
            category = None
        self._txt_start_time.SetValue(self.__strip_milliseconds(start))
        self._txt_end_time.SetValue(self.__strip_milliseconds(end  ))
        self._txt_name.SetValue(name)
        current_item_index = 0
        # Category Choice
        selection_set = False
        for cat in self._timeline.get_categories():
            self._lst_category.Append(cat.name, cat)
            if cat == category:
                self._lst_category.SetSelection(current_item_index)
                selection_set = True
            current_item_index += 1
        if not selection_set:
            self._lst_category.SetSelection(0)
        # Close on ok Checkbox
        self._cbx_close_on_ok.SetValue(True)

    def __set_initial_focus(self):
        """
        Set focus on the first empty textbox.

        If there is no empty textbox the focus is set to the 'start_time'
        textbox.
        """
        self._txt_start_time.SetFocus()
        for ctrl in [self._txt_start_time, self._txt_end_time,
                     self._txt_name]:
            if ctrl.GetValue().strip() == '':
                ctrl.SetFocus()
                break

    def __create_button_box(self):
        """
        Convenience method for creating a button box control.

        The control contains one OK button and one Close button.
        """
        button_box = wx.StdDialogButtonSizer()
        btn_ok = wx.Button(self, wx.ID_OK   )
        btn_close = wx.Button(self, wx.ID_CLOSE)
        btn_ok.SetDefault()
        button_box.SetCancelButton(btn_close)
        button_box.SetAffirmativeButton(btn_ok)
        button_box.Realize()
        self.Bind(wx.EVT_BUTTON, self.__btn_close_click, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.__btn_ok_click, btn_ok)
        self.Bind(wx.EVT_BUTTON, self.__btn_close_click, btn_close)
        self.SetEscapeId(btn_close.GetId())
        self.SetDefaultItem(btn_ok)
        self.SetAffirmativeId(btn_ok.GetId())
        return button_box

    def __strip_milliseconds(self, time_string):
        """
        Return the time string with milliseconds removed.

        Expected formt of time_string: yyyy-mm-dd-hh:mm:ss.mmmmmm
        """
        if time_string:
            return time_string.split('.')[0]
        else:
            return ''

    def __btn_close_click(self, evt):
        """
        Close the dialog.

        This event is triggered by one of the following actions:
          * Click the Close button
          * Press the Escape key
          * Click the dialog (X) button
        """
        logging.debug("__btn_close_click")
        self.__close()

    def __btn_ok_click(self, evt):
        """
        Add new or update existing event.

        If the Close-on-ok checkbox is checked the dialog is also closed.
        """
        logging.debug("__btn_ok_click")
        try:
            # Input value retrieval and validation
            start_time = parse_time_from_textbox(self._txt_start_time,
                                                 "start_time")
            end_time = parse_time_from_textbox(self._txt_end_time,
                                               "end_time")
            name = parse_text_from_textbox (self._txt_name, "Name")
            selection = self._lst_category.GetSelection()
            if selection >= 0:
                category = self._lst_category.GetClientData(selection)
            else:
                category = None
            if start_time > end_time:
                raise TxtException, ("End must be > Start", self._txt_start_time)
            # Update existing event
            if self._updatemode:
                self._event.update(start_time, end_time, name, category)
                self._timeline.event_edited(self._event)
            # Create new event
            else:
                self._event = Event(start_time, end_time, name, category)
                self._timeline.add_event(self._event)
            # Close the dialog ?
            if self._cbx_close_on_ok.GetValue():
                self.__close()
        except TxtException, ex:
            display_error_message("%s" % ex.error_message)
            set_focus_on_textctrl(ex.control)

    def __close(self):
        """
        Close the dialog.

        Make sure that no events are selected after the dialog is closed.
        """
        if self._event != None:
            self._event.selected = False
        self.EndModal(wx.ID_OK)


class CategoriesEditor(wx.Dialog):
    """This dialog is used for editing categories of a timeline."""

    def __init__(self, parent, timeline):
        wx.Dialog.__init__(self, parent, title="Edit Categories")
        self.timeline = timeline
        self.__create_gui()
        for category in self.timeline.get_categories():
            self.__add_category_to_list(category)

    def __create_gui(self):
        # The list box
        self.lst_categories = wx.ListBox(self, size=(200, 180),
                                         style=wx.LB_SINGLE|wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.__lst_categories_dclick,
                  self.lst_categories)
        # The Add button
        btn_add = wx.Button(self, wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, self.__btn_add_click, btn_add)
        # The Delete button
        btn_del = wx.Button(self, wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.__btn_del_click, btn_del)
        # The close button
        btn_close = wx.Button(self, wx.ID_CLOSE)
        btn_close.SetDefault()
        btn_close.SetFocus()
        self.SetAffirmativeId(wx.ID_CLOSE)
        # Setup layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.lst_categories, flag=wx.ALL|wx.EXPAND, border=BORDER)
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(btn_add, flag=wx.RIGHT, border=BORDER)
        button_box.Add(btn_del, flag=wx.RIGHT, border=BORDER)
        button_box.AddStretchSpacer()
        button_box.Add(btn_close, flag=wx.LEFT, border=BORDER)
        vbox.Add(button_box, flag=wx.ALL|wx.EXPAND, border=BORDER)
        self.SetSizerAndFit(vbox)
        self.lst_categories.SetFocus()

    def __add_category_to_list(self, category):
        self.lst_categories.Append(category.name, category)

    def __lst_categories_dclick(self, e):
        selection = e.GetSelection()
        dialog = CategoryEditor(self, self.timeline, e.GetClientData())
        if dialog.ShowModal() == wx.ID_OK:
            self.lst_categories.SetString(selection, dialog.category.name)
            self.timeline.category_edited(dialog.category)
        dialog.Destroy()

    def __btn_add_click(self, e):
        dialog = CategoryEditor(self, self.timeline, None)
        if dialog.ShowModal() == wx.ID_OK:
            self.__add_category_to_list(dialog.category)
            self.timeline.add_category(dialog.category)
        dialog.Destroy()

    def __btn_del_click(self, e):
        selection = self.lst_categories.GetSelection()
        if selection != wx.NOT_FOUND:
            ok_to_delete = wx.MessageBox('Are you sure to delete?', 'Question',
                              wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT, self) == wx.YES
            if ok_to_delete:
                cat = self.lst_categories.GetClientData(selection)
                self.timeline.delete_category(cat)
                self.lst_categories.Delete(selection)


class CategoryEditor(wx.Dialog):
    """This dialog is used for editing a category."""

    def __init__(self, parent, timeline, category):
        wx.Dialog.__init__(self, parent, title="Edit Category")
        self.timeline = timeline
        self.category = category
        self.__create_gui()
        if not self.category:
            self.category = Category("", (200, 200, 200))
        self.txt_name.SetValue(self.category.name)
        self.colorpicker.SetColour(self.category.color)

    def __create_gui(self):
        # The name text box
        self.txt_name = wx.TextCtrl(self, size=(150, -1))
        # The color chooser
        self.colorpicker = colourselect.ColourSelect(self)
        # Setup layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        # Grid for controls
        field_grid = wx.FlexGridSizer(2, 2, BORDER, BORDER)
        field_grid.Add(wx.StaticText(self, label="Name:"),
                       flag=wx.ALIGN_CENTER_VERTICAL)
        field_grid.Add(self.txt_name)
        field_grid.Add(wx.StaticText(self, label="Color:"),
                       flag=wx.ALIGN_CENTER_VERTICAL)
        field_grid.Add(self.colorpicker)
        vbox.Add(field_grid, flag=wx.EXPAND|wx.ALL, border=BORDER)
        # Buttons
        button_box = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self.__btn_ok_click, id=wx.ID_OK)
        vbox.Add(button_box, flag=wx.ALL|wx.EXPAND, border=BORDER)
        self.SetSizerAndFit(vbox)
        set_focus_on_textctrl(self.txt_name)

    def __verify_name(self):
        for cat in self.timeline.get_categories():
            if cat != self.category and cat.name == self.txt_name.GetValue():
                return False
        return True

    def __btn_ok_click(self, e):
        name = self.txt_name.GetValue()
        if self.__verify_name():
            self.category.name = name
            self.category.color = self.colorpicker.GetColour()
            self.EndModal(wx.ID_OK)
        else:
            display_error_message("Category name '%s' already in use." % name,
                                  self)


class TxtException(ValueError):
    """
    Thrown if a text control contains an invalid value.

    The constructor takes two arguments.

    The first is a text string containing any exception text.
    The seocond is a TextCtrl object.
    """
    def __init__(self, error_message, control):
        ValueError.__init__(self, error_message)
        self.error_message = error_message
        self.control = control


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
    """Open a dialog for creating a new event."""
    dlg = EventEditor(None, -1, 'Create Event', timeline, start, end)
    rv = dlg.ShowModal()
    dlg.Destroy()
    return rv


def edit_event(timeline, event):
    """Open a dialog for updating properties of a marked event"""
    dlg = EventEditor(None, -1, 'Edit Event', timeline, event=event)
    dlg.ShowModal()
    dlg.Destroy()


def edit_categories(timeline):
    dialog = CategoriesEditor(None, timeline)
    dialog.ShowModal()
    dialog.Destroy()


def set_focus_on_textctrl(txt):
    txt.SetFocus()
    txt.SelectAll()


def parse_text_from_textbox(txt, name):
    """
    Return a text control field.

    If the value is an empty string the method raises a ValueError
    exception and sets foucs on the control.

    If the value is valid the text in the control is returned
    """
    data = txt.GetValue().strip()
    if len(data) == 0:
        raise TxtException, ("%s: Can't be empty" % name, txt)
    return data


def parse_time_from_textbox(txt, name):
    """
    Convert a text string into a time value.

    If the value is not a valid time format a ValueError exception is
    raised and foucs is set on the control.

    If the text value is valid the text is converted into a  time value
    and thereafter returned.
    """
    try:
        time = todt(txt.GetValue())
    except:
        raise TxtException, ("Invalid %s data format.\n" % name +
                        "Expected format: yyyy-mm-dd:hh:mm:ss" , txt)
    return time


def display_error_message(message, parent=None):
    """Display an error message in a modal dialog box"""
    dial = wx.MessageDialog(parent, message, 'Error', wx.OK | wx.ICON_ERROR)
    dial.ShowModal()


def step_function(x_value):
    """
    A step function.

            {-1   when x < 0
    F(x) =  { 0   when x = 0
            { 1   when x > 0
    """
    y_value = 0
    if x_value < 0:
        y_value = -1
    elif x_value > 0:
        y_value = 1
    return y_value
