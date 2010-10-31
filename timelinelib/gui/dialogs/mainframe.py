# Copyright (C) 2009, 2010  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.


"""
The main frame of the application.
"""


import os.path
from datetime import datetime as dt
import datetime

import wx

from timelinelib.db import db_open
from timelinelib.db.interface import TimelineIOError
from timelinelib.gui.utils import WildcardHelper
from timelinelib.gui.utils import _display_error_message
from timelinelib.gui.utils import _ask_question
from timelinelib import config
from timelinelib.about import display_about_dialog
from timelinelib.about import APPLICATION_NAME
from timelinelib.paths import ICONS_DIR
from timelinelib.paths import HELP_RESOURCES_DIR
import timelinelib.printing as printing
import timelinelib.gui.utils as gui_utils
from timelinelib.gui.utils import BORDER
from timelinelib.gui.utils import ID_ERROR
from timelinelib.gui.dialogs.categorieseditor import CategoriesEditor
from timelinelib.gui.dialogs.duplicateevent import DuplicateEvent
from timelinelib.gui.dialogs.eventeditor import EventEditor
from timelinelib.gui.dialogs.gotodate import GotoDateDialog
from timelinelib.gui.dialogs.helpbrowser import HelpBrowser
from timelinelib.gui.dialogs.preferences import PreferencesDialog
from timelinelib.gui.components.cattree import CategoriesTree
from timelinelib.gui.components.hyperlinkbutton import HyperlinkButton
from timelinelib.gui.components.timelineview import DrawingArea
from timelinelib.gui.components.search import SearchBar
from timelinelib.utils import ex_msg


STATUS_READ_ONLY = 1


class MainFrame(wx.Frame):
    """
    The main frame of the application.

    Can be resized, maximized and minimized. Contains one panel: MainPanel.

    Owns an instance of a timeline that is currently being displayed. When the
    timeline changes, this control will notify sub controls about it.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, size=config.get_window_size(), 
                          pos=config.get_window_pos(),
                          style=wx.DEFAULT_FRAME_STYLE)
        # To enable translations of wx stock items.
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
        self._set_initial_values_to_member_variables()
        self.creating_gui = True
        self._create_gui()
        self.creating_gui = False
        self.Maximize(config.get_window_maximized())
        self.SetTitle(APPLICATION_NAME)
        self.mnu_view_sidebar.Check(config.get_show_sidebar())
        self.mnu_view_legend.Check(config.get_show_legend())
        self.mnu_view_balloons.Check(config.get_balloon_on_hover())
        self.SetIcons(self._load_icon_bundle())
        self._init_help_system()
        self.main_panel.show_welcome_panel()
        self.enable_disable_menus()
        self.controller = MainFrameController(self, db_open, config.global_config)

    def open_timeline(self, input_file):
        self.controller.open_timeline(input_file)
        self._create_navigation_menu_items()

    def open_timeline_if_exists(self, path):
        if os.path.exists(path):
            self.open_timeline(path)
        else:
            _display_error_message(_("File '%s' does not exist.") % path, self)

    def create_new_event(self, start=None, end=None):
        def create_event_editor():
            return EventEditor(self, _("Create Event"), self.timeline,
                               start, end)
        gui_utils.show_modal(create_event_editor, self.handle_db_error)

    def duplicate_event(self, event=None):
        """
        Duplicates the given event one or more times.
        
        If the given event == None, the selected event is duplicated.
        This happens when the main menu 'duplicate selected event' is used.
        This menu item is only enabled when there is only one event selected.
        The event is given as an argument when the event context menu item
        'duplicate event' is used.
        """
        def show_dialog(event):
            def create_dialog():
                return DuplicateEvent(self, self.timeline, event)
            gui_utils.show_modal(create_dialog, self.handle_db_error)
        if event is None:
            try:
                drawing_area = self.main_panel.drawing_area 
                id = drawing_area.get_view_properties().get_selected_event_ids()[0]
                event = self.timeline.find_event_with_id(id)
            except IndexError, e:
                # No event selected so do nothing!
                return
        show_dialog(event)

    def edit_event(self, event):
        def create_event_editor():
            return EventEditor(self, _("Edit Event"), self.timeline,
                               event=event)
        gui_utils.show_modal(create_event_editor, self.handle_db_error)

    def edit_categories(self):
        def create_categories_editor():
            return CategoriesEditor(self, self.timeline)
        gui_utils.show_modal(create_categories_editor, self.handle_db_error)

    def handle_db_error(self, error):
        """
        Should be called whenever a TimelineIOError was raised.
        """
        _display_error_message(ex_msg(error), self)
        self._switch_to_error_view(error)

    def _create_gui(self):
        def add_ellipses_to_menuitem(id):
            plain = wx.GetStockLabel(id,
                    wx.STOCK_WITH_ACCELERATOR|wx.STOCK_WITH_MNEMONIC)
            # format of plain 'xxx[\tyyy]', example '&New\tCtrl+N'
            tab_index = plain.find("\t")
            if tab_index != -1:
                return plain[:tab_index] + "..." + plain[tab_index:]
            return plain + "..."
        # The only content of this frame is the MainPanel
        self.main_panel = MainPanel(self)
        self.Bind(wx.EVT_CLOSE, self._window_on_close)
        # The status bar
        self.CreateStatusBar()
        self.GetStatusBar().SetFieldsCount(2)
        self.GetStatusBar().SetStatusWidths([-1, 200])
        # The menu
        # File menu
        self.mnu_file = wx.Menu()
        mnu_file_new = wx.Menu()
        accel = wx.GetStockLabel(wx.ID_NEW, wx.STOCK_WITH_ACCELERATOR|wx.STOCK_WITH_MNEMONIC)
        accel = accel.split("\t", 1)[1]
        self.mnu_file_new_file = mnu_file_new.Append(wx.ID_NEW, 
                                                     _("File Timeline...") + "\t" + accel, 
                                                     _("File Timeline..."))
        self.mnu_file_new_dir = mnu_file_new.Append(wx.ID_ANY, 
                                                    _("Directory Timeline..."), 
                                                    _("Directory Timeline..."))
        self.mnu_file.AppendMenu(wx.ID_ANY, _("New"), mnu_file_new,
                                 _("Create a new timeline"))
        self.mnu_file.Append(wx.ID_OPEN, add_ellipses_to_menuitem(wx.ID_OPEN),
                             _("Open an existing timeline"))
        self.mnu_file_open_recent_submenu = wx.Menu()
        self.mnu_file.AppendMenu(wx.ID_ANY, _("Open &Recent"), self.mnu_file_open_recent_submenu)
        self._update_open_recent_submenu()
        self.mnu_file.AppendSeparator()
        self.mnu_file_print_setup = self.mnu_file.Append(wx.ID_PRINT_SETUP,
                                       _("Page Set&up..."),
                                       _("Setup page for printing"))
        self.mnu_file_print_preview = self.mnu_file.Append(wx.ID_PREVIEW, "",
                                       _("Print Preview"))
        self.mnu_file_print = self.mnu_file.Append(wx.ID_PRINT,
                                       add_ellipses_to_menuitem(wx.ID_PRINT),
                                       _("Print"))
        self.mnu_file.AppendSeparator()
        self.mnu_file_export = self.mnu_file.Append(wx.ID_ANY,
                                                   _("&Export to Image..."),
                                                   _("Export the current view to a PNG image"))
        self.mnu_file.AppendSeparator()
        self.mnu_file.Append(wx.ID_EXIT, "",
                             _("Exit the program"))
        self.Bind(wx.EVT_MENU, self._mnu_file_new_on_click, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self._mnu_file_new_dir_on_click, self.mnu_file_new_dir)
        self.Bind(wx.EVT_MENU, self._mnu_file_open_on_click, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._mnu_file_print_on_click, id=wx.ID_PRINT)
        self.Bind(wx.EVT_MENU, self._mnu_file_print_preview_on_click, id=wx.ID_PREVIEW)
        self.Bind(wx.EVT_MENU, self._mnu_file_print_setup_on_click, id=wx.ID_PRINT_SETUP)
        self.Bind(wx.EVT_MENU, self._mnu_file_export_on_click,
                  self.mnu_file_export)
        self.Bind(wx.EVT_MENU, self._mnu_file_exit_on_click, id=wx.ID_EXIT)
        # Edit menu
        self.mnu_edit = wx.Menu()
        self.mnu_edit_find = self.mnu_edit.Append(wx.ID_FIND)
        self.Bind(wx.EVT_MENU, self._mnu_edit_find_on_click,
                  self.mnu_edit_find)
        self.mnu_edit.AppendSeparator()
        mnu_edit_preferences = self.mnu_edit.Append(wx.ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self._mnu_edit_preferences_on_click,
                  mnu_edit_preferences)
        # Timeline menu
        self.mnu_timeline = wx.Menu()
        self.mnu_timeline_create_event = self.mnu_timeline.Append(wx.ID_ANY,
                                    _("Create &Event..."),
                                    _("Create a new event"))
        self.mnu_timeline_duplicate_event = self.mnu_timeline.Append(wx.ID_ANY,
                                    _("&Duplicate Selected Event..."),
                                    _("Duplicate the Selected Event"))
        self.mnu_timeline_edit_categories = self.mnu_timeline.Append(wx.ID_ANY,
                                       _("Edit &Categories"),
                                       _("Edit categories"))
        self.Bind(wx.EVT_MENU, self._mnu_timeline_create_event_on_click,
                  self.mnu_timeline_create_event)
        self.Bind(wx.EVT_MENU, self._mnu_timeline_duplicate_event_on_click,
                  self.mnu_timeline_duplicate_event)
        self.Bind(wx.EVT_MENU, self._mnu_timeline_edit_categories_on_click,
                  self.mnu_timeline_edit_categories)
        # View menu
        self.mnu_view = wx.Menu()
        self.mnu_view_sidebar = self.mnu_view.Append(wx.ID_ANY,
                                                     _("&Sidebar\tCtrl+I"),
                                                     kind=wx.ITEM_CHECK)
        self.mnu_view_legend = self.mnu_view.Append(wx.ID_ANY,
                                                    _("&Legend"),
                                                    kind=wx.ITEM_CHECK)
        self.mnu_view.AppendSeparator()
        self.mnu_view_balloons = self.mnu_view.Append(wx.ID_ANY,
                                                    _("&Balloons on hover"),
                                                    kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self._mnu_view_sidebar_on_click,
                  self.mnu_view_sidebar)
        self.Bind(wx.EVT_MENU, self._mnu_view_legend_on_click,
                  self.mnu_view_legend)
        self.Bind(wx.EVT_MENU, self._mnu_view_balloons_on_click,
                  self.mnu_view_balloons)
        # Navigate menu
        self.mnu_navigate = wx.Menu()
        self._navigation_menu_items = []
        self._create_navigation_menu_items()
        self.mnu_navigate.AppendSeparator()
        find_first = self.mnu_navigate.Append(wx.ID_ANY, _("Find First Event"))
        find_last  = self.mnu_navigate.Append(wx.ID_ANY, _("Find Last Event"))
        fit_all_events = self.mnu_navigate.Append(wx.ID_ANY, _("Fit All Events"))
        self.Bind(wx.EVT_MENU, self._mnu_navigate_find_first_on_click, find_first)
        self.Bind(wx.EVT_MENU, self._mnu_navigate_find_last_on_click, find_last)
        self.Bind(wx.EVT_MENU, self._mnu_navigate_fit_all_events_on_click, fit_all_events)
        # Help menu
        self.mnu_help = wx.Menu()
        help_contents = self.mnu_help.Append(wx.ID_HELP, _("&Contents\tF1"))
        self.Bind(wx.EVT_MENU, self._mnu_help_contents_on_click, help_contents)
        self.mnu_help.AppendSeparator()
        help_tutorial = self.mnu_help.Append(wx.ID_ANY, _("Getting started tutorial"))
        self.Bind(wx.EVT_MENU, self._mnu_help_tutorial_on_click, help_tutorial)
        help_contact = self.mnu_help.Append(wx.ID_ANY, _("Contact"))
        self.Bind(wx.EVT_MENU, self._mnu_help_contact_on_click, help_contact)
        self.mnu_help.AppendSeparator()
        help_about = self.mnu_help.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self._mnu_help_about_on_click, help_about)
        # The menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(self.mnu_file, _("&File"))
        menuBar.Append(self.mnu_edit, _("&Edit"))
        menuBar.Append(self.mnu_view, _("&View"))
        menuBar.Append(self.mnu_timeline, _("&Timeline"))
        menuBar.Append(self.mnu_navigate, _("&Navigate"))
        menuBar.Append(self.mnu_help, _("&Help"))
        self.SetMenuBar(menuBar)

    def _create_navigation_menu_items(self):
        self._clear_navigation_menu_items()
        def go_to_today_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.center(dt.now()))
        def go_to_date_fn(main_frame, current_period, navigation_fn):
            dialog = GotoDateDialog(main_frame, current_period.mean_time())
            if dialog.ShowModal() == wx.ID_OK:
                navigation_fn(lambda tp: tp.center(dialog.time))
            dialog.Destroy()
        def backward_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.move_page_smart(-1))
        def forward_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.move_page_smart(1))
        def forward_one_week_fn(main_frame, current_period, navigation_fn):
            wk = datetime.timedelta(days=7)
            navigation_fn(lambda tp: tp.move_delta(wk))
        def backward_one_week_fn(main_frame, current_period, navigation_fn):
            wk = datetime.timedelta(days=7)
            navigation_fn(lambda tp: tp.move_delta(-1*wk))
        def navigate_month_step(current_period, navigation_fn, direction):
            """
            Currently does notice leap years.
            """
            tm = current_period.mean_time()
            if direction > 0:
                if tm.month == 2:
                    d = 28
                elif tm.month in (4,6,9,11):
                    d = 30
                else:
                    d = 31
            else:
                if tm.month == 3:
                    d = 28
                elif tm.month in (5,7,10,12):
                    d = 30
                else:
                    d = 31
            mv = datetime.timedelta(days=d)
            navigation_fn(lambda tp: tp.move_delta(direction*mv))
        def forward_one_month_fn(main_frame, current_period, navigation_fn):
            navigate_month_step(current_period, navigation_fn, 1)
        def backward_one_month_fn(main_frame, current_period, navigation_fn):
            navigate_month_step(current_period, navigation_fn, -1)
        def forward_one_year_fn(main_frame, current_period, navigation_fn):
            yr = datetime.timedelta(days=365)
            navigation_fn(lambda tp: tp.move_delta(yr))
        def backward_one_year_fn(main_frame, current_period, navigation_fn):
            yr = datetime.timedelta(days=365)
            navigation_fn(lambda tp: tp.move_delta(-1*yr))
        def fit_millennium_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_millennium())
        def fit_century_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_century())
        def fit_decade_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_decade())
        def fit_year_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_year())
        def fit_month_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_month())
        def fit_day_fn(main_frame, current_period, navigation_fn):
            navigation_fn(lambda tp: tp.fit_day())
        item_data = [
            (_("Go to &Today\tCtrl+T"), go_to_today_fn),
            (_("Go to D&ate...\tCtrl+G"), go_to_date_fn),
            ("SEP", None),
            (_("Backward\tPgUp"), backward_fn),
            (_("Forward\tPgDn"), forward_fn),
            (_("Forward One Wee&k\tCtrl+K"), forward_one_week_fn),
            (_("Back One &Week\tCtrl+W"), backward_one_week_fn),
            (_("Forward One Mont&h\tCtrl+h"), forward_one_month_fn),
            (_("Back One &Month\tCtrl+M"), backward_one_month_fn),
            (_("Forward One Yea&r\tCtrl+R"), forward_one_year_fn),
            (_("Back One &Year\tCtrl+Y"), backward_one_year_fn),
            ("SEP", None),
            (_("Fit Millennium"), fit_millennium_fn),
            (_("Fit Century"), fit_century_fn),
            (_("Fit Decade"), fit_decade_fn),
            (_("Fit Year"), fit_year_fn),
            (_("Fit Month"), fit_month_fn),
            (_("Fit Day"), fit_day_fn),
        ]
        self._navigation_menu_items_map = {}
        pos = 0
        for (itemstr, fn) in item_data:
            if itemstr == "SEP":
                item = self.mnu_navigate.InsertSeparator(pos)
            else:
                item = self.mnu_navigate.Insert(pos, wx.ID_ANY, itemstr)
                self._navigation_menu_items_map[item.GetId()] = fn
                self.Bind(wx.EVT_MENU, self._on_nav_menu_item_click, item)
            self._navigation_menu_items.append(item)
            pos += 1

    def _on_nav_menu_item_click(self, evt):
        fn = self._navigation_menu_items_map[evt.GetId()]
        fn(self, self._get_time_period(), self._navigate_timeline)

    def _clear_navigation_menu_items(self):
        while self._navigation_menu_items:
            self.mnu_navigate.RemoveItem(self._navigation_menu_items.pop())

    def _update_open_recent_submenu(self):
        # Clear items
        for item in self.mnu_file_open_recent_submenu.GetMenuItems():
            self.mnu_file_open_recent_submenu.DeleteItem(item)
        # Create new items and map (item id > path)
        self.open_recent_map = {}
        for path in config.get_recently_opened():
            name = "%s (%s)" % (
                os.path.basename(path),
                os.path.dirname(os.path.abspath(path)))
            item = self.mnu_file_open_recent_submenu.Append(wx.ID_ANY, name)
            self.open_recent_map[item.GetId()] = path
            self.Bind(wx.EVT_MENU, self._mnu_file_open_recent_item_on_click,
                      item)

    def _window_on_close(self, event):
        self._save_current_timeline_data()
        self._save_application_config()
        self.Destroy()

    def _mnu_file_new_on_click(self, event):
        """Event handler used when the user wants to create a new timeline."""
        self._create_new_timeline()

    def _mnu_file_new_dir_on_click(self, event):
        self._create_new_dir_timeline()

    def _mnu_file_open_on_click(self, event):
        """Event handler used when the user wants to open a new timeline."""
        self._open_existing_timeline()

    def _mnu_file_open_recent_item_on_click(self, event):
        path = self.open_recent_map[event.GetId()]
        self.open_timeline_if_exists(path)

    def _mnu_file_print_on_click(self, event):
        self.main_panel.drawing_area.print_timeline(event)

    def _mnu_file_print_preview_on_click(self, event):
        self.main_panel.drawing_area.print_preview(event)

    def _mnu_file_print_setup_on_click(self, event):
        self.main_panel.drawing_area.print_setup(event)

    def _mnu_file_export_on_click(self, evt):
        self._export_to_image()

    def _mnu_file_exit_on_click(self, evt):
        """Event handler for the Exit menu item"""
        self.Close()

    def _mnu_edit_find_on_click(self, evt):
        self.main_panel.show_searchbar(True)

    def _mnu_edit_preferences_on_click(self, evt):
        dialog = PreferencesDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def _mnu_view_sidebar_on_click(self, evt):
        if evt.IsChecked():
            self.main_panel.show_sidebar()
        else:
            self.main_panel.hide_sidebar()

    def _mnu_view_legend_on_click(self, evt):
        self.main_panel.drawing_area.show_hide_legend(evt.IsChecked())

    def _mnu_view_balloons_on_click(self, evt):
        config.set_balloon_on_hover(evt.IsChecked())
        self.main_panel.drawing_area.balloon_visibility_changed(evt.IsChecked())

    def _mnu_timeline_create_event_on_click(self, evt):
        self.create_new_event()

    def _mnu_timeline_duplicate_event_on_click(self, evt):
        self.duplicate_event()

    def _mnu_timeline_edit_categories_on_click(self, evt):
        self.edit_categories()

    def _mnu_navigate_find_first_on_click(self, evt):
        event = self.timeline.get_first_event()
        if event:
            start = event.time_period.start_time
            delta = self.main_panel.drawing_area.get_view_properties().displayed_period.delta()
            end   = start + delta 
            margin_delta = delta / 24
            self._navigate_timeline(lambda tp: tp.update(start, end, -margin_delta))

    def _mnu_navigate_find_last_on_click(self, evt):
        event = self.timeline.get_last_event()
        if event:
            end = event.time_period.end_time
            delta = self.main_panel.drawing_area.get_view_properties().displayed_period.delta()
            start = end - delta
            margin_delta = delta / 24
            self._navigate_timeline(lambda tp: tp.update(start, end, 
                                                       end_delta=margin_delta))

    def _mnu_navigate_fit_all_events_on_click(self, evt):
        firstEvent = self.timeline.get_first_event()
        lastEvent  = self.timeline.get_last_event()
        try:
            if firstEvent == lastEvent:
                mean = firstEvent.time_period.mean_time()
                self._navigate_timeline(lambda tp: tp.center(mean))
            else:
                start = firstEvent.time_period.start_time
                end   = lastEvent.time_period.end_time
                margin_delta = (end - start) / 24
                self._navigate_timeline(lambda tp: tp.update(start, end, -margin_delta, margin_delta))
        except AttributeError:
            # None events
            pass        
        except:
            raise
    
    def _mnu_help_contents_on_click(self, e):
        self.show_help_page("contents")

    def _mnu_help_tutorial_on_click(self, e):
        self.open_timeline(":tutorial:")

    def _mnu_help_contact_on_click(self, e):
        self.show_help_page("contact")

    def _mnu_help_about_on_click(self, e):
        display_about_dialog()

    def show_help_page(self, page):
        if self.help_browser is None:
            _display_error_message(_("Could not find markdown Python package.  It is needed by the help system. See the Timeline website or the INSTALL file for instructions how to install it."), self)
        else:
            self.help_browser.show_page(page)

    def _init_help_system(self):
        try:
            import markdown
        except ImportError:
            self.help_browser = None
        else:
            import timelinelib.help as help
            import timelinelib.help_pages as help_pages
            help_system = help.HelpSystem("contents", HELP_RESOURCES_DIR + "/",
                                          "page:")
            help_pages.install(help_system)
            self.help_browser = HelpBrowser(self, help_system)

    def _switch_to_error_view(self, error):
        self._display_timeline(None)
        self.main_panel.error_panel.populate(error)
        self.main_panel.show_error_panel()
        self.enable_disable_menus()

    def _display_timeline(self, timeline):
        self.timeline = timeline
        if timeline == None:
            # Do this before the next line so that we still have a timeline to
            # unregister
            self.main_panel.cattree.initialize_from_timeline_view(None)
            self.main_panel.searchbar.set_view(None)
        self.main_panel.drawing_area.set_timeline(self.timeline)
        self.GetStatusBar().SetStatusText("", STATUS_READ_ONLY)
        if timeline == None:
            self.main_panel.show_welcome_panel()
            self.SetTitle(APPLICATION_NAME)
        else:
            self.main_panel.cattree.initialize_from_timeline_view(self.main_panel.drawing_area)
            self.main_panel.searchbar.set_view(self.main_panel.drawing_area)
            self.main_panel.show_timeline_panel()
            self.SetTitle("%s (%s) - %s" % (
                os.path.basename(self.timeline.path),
                os.path.dirname(os.path.abspath(self.timeline.path)),
                APPLICATION_NAME))
            if timeline.is_read_only():
                self.GetStatusBar().SetStatusText(_("read-only"), STATUS_READ_ONLY)

    def _create_new_timeline(self):
        """
        Create a new empty timeline.

        The user is asked to enter the filename of the new timeline to be
        created.

        If the new filename entered, should already exist, the existing
        timeline is opened. The user will be informed about this situation.
        """
        wildcard = self.timeline_wildcard_helper.wildcard_string()
        dialog = wx.FileDialog(self, message=_("Create Timeline"),
                               wildcard=wildcard, style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self._save_current_timeline_data()
            path = self.timeline_wildcard_helper.get_path(dialog)
            if os.path.exists(path):
                msg_first_part = _("The specified timeline already exists.")
                msg_second_part = _("Opening timeline instead of creating new.")
                wx.MessageBox("%s\n\n%s" % (msg_first_part, msg_second_part),
                              _("Information"),
                              wx.OK|wx.ICON_INFORMATION, self)
            self.open_timeline(path)
        dialog.Destroy()

    def _create_new_dir_timeline(self):
        """
        Create a new empty timeline.

        The user is asked to enter the path to a dircetory from which files are
        to be read.

        If the new path entered, should already exist, the existing
        timeline is opened. The user will be informed about this situation.
        """
        dialog = wx.DirDialog(self, message=_("Create Timeline"))
        if dialog.ShowModal() == wx.ID_OK:
            self._save_current_timeline_data()
            self.open_timeline(dialog.GetPath())
        dialog.Destroy()

    def _open_existing_timeline(self):
        """
        Open a new timeline.

        The user is asked to enter the filename of the timeline to be opened.
        """
        dir = ""
        if self.timeline is not None:
            dir = os.path.dirname(self.timeline.path)
        wildcard = self.timeline_wildcard_helper.wildcard_string()
        dialog = wx.FileDialog(self, message=_("Open Timeline"),
                               defaultDir=dir,
                               wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self._save_current_timeline_data()
            self.open_timeline(dialog.GetPath())
        dialog.Destroy()

    def enable_disable_menus(self):
        """
        Enable or disable menu items depending on the state of the application.
        """
        if self.creating_gui:
            return
        items_requiring_timeline_view = [
            self.mnu_view_sidebar,
        ]
        items_requiring_timeline = [
            self.mnu_file_print,
            self.mnu_file_print_preview,
            self.mnu_file_print_setup,
            self.mnu_file_export,
            self.mnu_view_legend,
            self.mnu_edit_find,
        ]
        items_requiring_update = [
            self.mnu_timeline_create_event, 
            self.mnu_timeline_edit_categories, 
        ]
        for item in self.mnu_timeline.GetMenuItems():
            items_requiring_timeline.append(item)
        for item in self.mnu_navigate.GetMenuItems():
            items_requiring_timeline.append(item)
        have_timeline_view = self.main_panel.timeline_panel_visible()
        have_timeline = self.timeline != None
        is_read_only = have_timeline and self.timeline.is_read_only()     
        for item in items_requiring_timeline_view:
            item.Enable(have_timeline_view)
        for item in items_requiring_timeline:
            item.Enable(have_timeline)
        for item in items_requiring_update:
            item.Enable(not is_read_only)
        if not have_timeline:
            self.main_panel.show_searchbar(False)
        # One and only one event selected ?
        one_event_selected = len(self.main_panel.drawing_area.get_view_properties().selected_event_ids) == 1
        self.mnu_timeline_duplicate_event.Enable(one_event_selected)
        
    def _save_application_config(self):
        config.set_window_size(self.GetSize())
        config.set_window_pos(self.GetPosition())
        config.set_window_maximized(self.IsMaximized())
        config.set_show_sidebar(self.mnu_view_sidebar.IsChecked())
        config.set_show_legend(self.mnu_view_legend.IsChecked())
        config.set_sidebar_width(self.main_panel.get_sidebar_width())
        try:
            config.write()
        except IOError, ex:
            friendly = _("Unable to write configuration file.")
            msg = "%s\n\n%s" % (friendly, ex_msg(ex))
            _display_error_message(msg, self)

    def _save_current_timeline_data(self):
        """
        Saves settings for the timeline that is currently displayed to
        the timeline file. Date saved is:
            - currently displayed time period
        If there is no current timeline, nothing happens.
        This method should be called before a new timeline is opened
        or created or when the application is closed.
        """
        if self.timeline:
            try:
                self.timeline.save_view_properties(self.main_panel.drawing_area.get_view_properties())
            except TimelineIOError, e:
                self.handle_db_error(e)

    def _export_to_image(self):
        wildcard = self.images_wildcard_helper.wildcard_string()
        dialog = wx.FileDialog(self, message=_("Export to Image"),
                               wildcard=wildcard, style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            path = self.images_wildcard_helper.get_path(dialog)
            overwrite_question = _("File '%s' exists. Overwrite?") % path
            if (not os.path.exists(path) or
                _ask_question(overwrite_question, self) == wx.YES):
                bitmap = self.main_panel.drawing_area.get_current_image()
                image = wx.ImageFromBitmap(bitmap)
                type = self.images_wildcard_helper.get_extension_data(path)
                image.SaveFile(path, type)
        dialog.Destroy()

    def _set_initial_values_to_member_variables(self):
        """
        Instance variables usage:

        timeline            The timeline currently handled by the application
        """
        self.timeline = None
        self.timeline_wildcard_helper = WildcardHelper(
            _("Timeline files"), ["timeline", "ics"])
        self.images_wildcard_helper = WildcardHelper(
            _("Image files"), [("png", wx.BITMAP_TYPE_PNG)])

    def _load_icon_bundle(self):
        bundle = wx.IconBundle()
        for size in ["16", "32", "48"]:
            iconpath = os.path.join(ICONS_DIR, "%s.png" % size)
            icon = wx.IconFromBitmap(wx.BitmapFromImage(wx.Image(iconpath)))
            bundle.AddIcon(icon)
        return bundle

    def _navigate_timeline(self, navigation_fn):
        """Shortcut for method in DrawingArea."""
        return self.main_panel.drawing_area.navigate_timeline(navigation_fn)

    def _get_time_period(self):
        """Shortcut for method in DrawingArea."""
        return self.main_panel.drawing_area.get_time_period()


class MainFrameController(object):

    def __init__(self, main_frame, db_open_fn, config):
        self.main_frame = main_frame
        self.db_open_fn = db_open_fn
        self.config = config

    def open_timeline(self, path):
        """Read timeline info from the given input file and display it."""
        try:
            timeline = self.db_open_fn(path)
        except TimelineIOError, e:
            self.main_frame.handle_db_error(e)
        else:
            self.config.append_recently_opened(path)
            self.main_frame._update_open_recent_submenu()
            self.main_frame._display_timeline(timeline)


class MainPanel(wx.Panel):
    """
    Panel that covers the whole client area of MainFrame.

    Displays one of the following panels:

      * The welcome panel (show_welcome_panel)
      * A splitter with sidebar and DrawingArea (show_timeline_panel)
      * The error panel (show_error_panel)

    Also displays the search bar.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._create_gui()
        # Install variables for backwards compatibility
        self.cattree = self.timeline_panel.sidebar.cattree
        self.drawing_area = self.timeline_panel.drawing_area
        self.show_sidebar = self.timeline_panel.show_sidebar
        self.hide_sidebar = self.timeline_panel.hide_sidebar
        self.get_sidebar_width = self.timeline_panel.get_sidebar_width

    def timeline_panel_visible(self):
        return self.timeline_panel.IsShown()

    def show_welcome_panel(self):
        self._show_panel(self.welcome_panel)

    def show_timeline_panel(self):
        self._show_panel(self.timeline_panel)

    def show_error_panel(self):
        self._show_panel(self.error_panel)

    def show_searchbar(self, show=True):
        self.searchbar.Show(show)
        if show == True:
            self.searchbar.search.SetFocus()
        self.GetSizer().Layout()

    def _create_gui(self):
        # Search bar
        def search_close():
            self.show_searchbar(False)
        self.searchbar = SearchBar(self, search_close)
        self.searchbar.Show(False)
        # Panels
        self.welcome_panel = WelcomePanel(self)
        self.timeline_panel = TimelinePanel(self)
        self.error_panel = ErrorPanel(self)
        # Layout
        self.sizerOuter = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.welcome_panel, flag=wx.GROW, proportion=1)
        self.sizer.Add(self.timeline_panel, flag=wx.GROW, proportion=1)
        self.sizer.Add(self.error_panel, flag=wx.GROW, proportion=1)
        self.sizerOuter.Add(self.sizer, flag=wx.GROW, proportion=1)
        self.sizerOuter.Add(self.searchbar, flag=wx.GROW, proportion=0)
        self.SetSizer(self.sizerOuter)

    def _show_panel(self, panel):
        # Hide all panels
        for panel_to_hide in [self.welcome_panel, self.timeline_panel,
                              self.error_panel]:
            panel_to_hide.Show(False)
        # Show this one
        panel.Show(True)
        self.sizerOuter.Layout()


class WelcomePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._create_gui()

    def _create_gui(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        # Text 1
        t1 = wx.StaticText(self, label=_("No timeline opened."))
        vsizer.Add(t1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Spacer
        vsizer.AddSpacer(20)
        # Text 2
        t2 = wx.StaticText(self, label=_("First time using Timeline?"))
        vsizer.Add(t2, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Button
        btn_tutorial = HyperlinkButton(self, _("Getting started tutorial"))
        self.Bind(wx.EVT_HYPERLINK, self._btn_tutorial_on_click, btn_tutorial)
        vsizer.Add(btn_tutorial, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Sizer
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(vsizer, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, proportion=1)
        self.SetSizer(hsizer)

    def _btn_tutorial_on_click(self, e):
        wx.GetTopLevelParent(self).open_timeline(":tutorial:")


class TimelinePanel(wx.Panel):
    """
    Showing the drawn timeline, the vertical sizer, and the optional sidebar.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sidebar_width = config.get_sidebar_width()
        self._create_gui()
        self.show_sidebar()
        if not config.get_show_sidebar():
            self.hide_sidebar()

    def get_sidebar_width(self):
        return self.sidebar_width

    def show_sidebar(self):
        self.splitter.SplitVertically(self.sidebar, self.drawing_area,
                                      self.sidebar_width)

    def hide_sidebar(self):
        self.splitter.Unsplit(self.sidebar)

    def _create_gui(self):
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(50)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED,
                  self._splitter_on_splitter_sash_pos_changed, self.splitter)
        self.sidebar = Sidebar(self.splitter)
        self.divider_line_slider = wx.Slider(self, value = 50, size = (20, -1),
                                             style = wx.SL_LEFT | wx.SL_VERTICAL)
        main_frame = wx.GetTopLevelParent(self)
        self.drawing_area = DrawingArea(self.splitter,
                                        self.divider_line_slider,
                                        main_frame.handle_db_error)
        globalSizer = wx.BoxSizer(wx.HORIZONTAL)
        globalSizer.Add(self.splitter, 1, wx.EXPAND)
        globalSizer.Add(self.divider_line_slider, 0, wx.EXPAND)
        self.SetSizer(globalSizer)

    def _splitter_on_splitter_sash_pos_changed(self, e):
        self.sidebar_width = self.splitter.GetSashPosition()


class ErrorPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._create_gui()

    def populate(self, error):
        self.txt_error.SetLabel(ex_msg(error))

    def _create_gui(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        # Error text
        self.txt_error = wx.StaticText(self, label="")
        vsizer.Add(self.txt_error, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Spacer
        vsizer.AddSpacer(20)
        # Help text
        txt_help = wx.StaticText(self, label=_("Relevant help topics:"))
        vsizer.Add(txt_help, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Button
        btn_contact = HyperlinkButton(self, _("Contact"))
        self.Bind(wx.EVT_HYPERLINK, self._btn_contact_on_click, btn_contact)
        vsizer.Add(btn_contact, flag=wx.ALIGN_CENTER_HORIZONTAL)
        # Sizer
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(vsizer, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, proportion=1)
        self.SetSizer(hsizer)

    def _btn_contact_on_click(self, e):
        wx.GetTopLevelParent(self).show_help_page("contact")


class Sidebar(wx.Panel):
    """
    The left part in TimelinePanel.

    Currently only shows the categories with visibility check boxes.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_NONE)
        self._create_gui()

    def _create_gui(self):
        main_frame = wx.GetTopLevelParent(self)
        self.cattree = CategoriesTree(self, main_frame.handle_db_error)
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cattree, flag=wx.GROW, proportion=1)
        self.SetSizer(sizer)
