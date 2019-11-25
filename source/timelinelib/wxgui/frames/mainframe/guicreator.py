# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
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
A base class for the mainframe window, responsible for creating the GUI.
"""


import collections
import wx

from timelinelib.db.utils import safe_locking
from timelinelib.wxgui.components.mainpanel import MainPanel
from timelinelib.wxgui.components.statusbaradapter import StatusBarAdapter
from timelinelib.wxgui.dialogs.duplicateevent.view import open_duplicate_event_dialog_for_event
from timelinelib.wxgui.dialogs.editevent.view import open_create_event_editor
from timelinelib.wxgui.dialogs.filenew.view import FileNewDialog
from timelinelib.wxgui.dialogs.importevents.view import ImportEventsDialog
from timelinelib.wxgui.dialogs.milestone.view import open_milestone_editor_for
from timelinelib.wxgui.frames.mainframe.menus.filemenu import FileMenu
from timelinelib.wxgui.frames.mainframe.menus.editmenu import EditMenu
from timelinelib.wxgui.frames.mainframe.menus.viewmenu import ViewMenu
from timelinelib.wxgui.frames.mainframe.menus.helpmenu import HelpMenu
# The following imports are used by the shortcut module
from timelinelib.wxgui.frames.mainframe.menus.filemenu import ID_IMPORT
from timelinelib.wxgui.frames.mainframe.menus.editmenu import ID_SELECT_ALL, ID_FIND_CATEGORIES, ID_FIND_MILESTONES, ID_EDIT_SHORTCUTS
from timelinelib.wxgui.frames.mainframe.menus.viewmenu import ID_SIDEBAR, ID_LEGEND, ID_BALLOONS, ID_ZOOMIN, ID_ZOOMOUT, ID_VERT_ZOOMIN, ID_VERT_ZOOMOUT, ID_HIDE_DONE, ID_PRESENTATION
from timelinelib.wxgui.frames.mainframe.menus.helpmenu import ID_TUTORIAL, ID_NUMTUTORIAL, ID_FEEDBACK, ID_CONTACT, ID_SYSTEM_INFO

NONE = 0
CHECKBOX = 1
CHECKED_RB = 2
UNCHECKED_RB = 3
ID_CREATE_EVENT = wx.NewId()
ID_CREATE_MILESTONE = wx.NewId()
ID_PT_EVENT_TO_RIGHT = wx.NewId()
ID_EDIT_EVENT = wx.NewId()
ID_DUPLICATE_EVENT = wx.NewId()
ID_SET_CATEGORY_ON_SELECTED = wx.NewId()
ID_MEASURE_DISTANCE = wx.NewId()
ID_COMPRESS = wx.NewId()
ID_SET_CATEGORY_ON_WITHOUT = wx.NewId()
ID_EDIT_ERAS = wx.NewId()
ID_SET_READONLY = wx.NewId()
ID_FIND_FIRST = wx.NewId()
ID_FIND_LAST = wx.NewId()
ID_FIT_ALL = wx.NewId()
ID_EXPORT = wx.NewId()
ID_EXPORT_ALL = wx.NewId()
ID_EXPORT_SVG = wx.NewId()
ID_RESTORE_TIME_PERIOD = wx.NewId()
ID_NEW = wx.ID_NEW
ID_FIND = wx.ID_FIND
ID_UNDO = wx.NewId()
ID_REDO = wx.NewId()
ID_PREFERENCES = wx.ID_PREFERENCES
ID_HELP = wx.ID_HELP
ID_ABOUT = wx.ID_ABOUT
ID_SAVEAS = wx.ID_SAVEAS
ID_EXIT = wx.ID_EXIT
ID_MOVE_EVENT_UP = wx.NewId()
ID_MOVE_EVENT_DOWN = wx.NewId()
ID_NAVIGATE = wx.NewId() + 100


class GuiCreator:

    def _create_gui(self):
        self.shortcut_items = {}
        from timelinelib.config.shortcut import ShortcutController
        self.shortcut_controller = ShortcutController(self.config, self.shortcut_items)
        self._create_status_bar()
        self._create_main_panel()
        self._create_main_menu_bar()
        self._bind_frame_events()

    def _create_status_bar(self):
        self.CreateStatusBar()
        self.status_bar_adapter = StatusBarAdapter(self.GetStatusBar())

    def _create_main_panel(self):
        self.main_panel = MainPanel(self, self.config, self)

    def _create_main_menu_bar(self):
        main_menu_bar = wx.MenuBar()
        main_menu_bar.Append(FileMenu(self).create(), _("&File"))
        main_menu_bar.Append(EditMenu(self).create(), _("&Edit"))
        main_menu_bar.Append(ViewMenu(self).create(), _("&View"))
        main_menu_bar.Append(self._create_timeline_menu(), _("&Timeline"))
        main_menu_bar.Append(self._create_navigate_menu(), _("&Navigate"))
        main_menu_bar.Append(HelpMenu(self).create(), _("&Help"))
        self._set_shortcuts()
        self.SetMenuBar(main_menu_bar)
        self.update_navigation_menu_items()
        self.enable_disable_menus()

    def _set_shortcuts(self):
        self.shortcut_controller.load_config_settings()

    def _bind_frame_events(self):
        self.Bind(wx.EVT_CLOSE, self._window_on_close)

    def set_category_on_selected(self):

        def edit_function():
            self._set_category_to_selected_events()

        safe_locking(self, edit_function)

    def _create_timeline_menu(self):

        def create_event(evt):
            open_create_event_editor(self, self, self.config, self.timeline)

        def edit_event(evt):
            try:
                event_id = self.main_panel.get_id_of_first_selected_event()
                event = self.timeline.find_event_with_id(event_id)
            except IndexError:
                # No event selected so do nothing!
                return
            self.main_panel.open_event_editor(event)

        def duplicate_event(evt):
            try:
                event_id = self.main_panel.get_id_of_first_selected_event()
                event = self.timeline.find_event_with_id(event_id)
            except IndexError:
                # No event selected so do nothing!
                return
            open_duplicate_event_dialog_for_event(self, self, self.timeline, event)

        def create_milestone(evt):
            open_milestone_editor_for(self, self, self.config, self.timeline)

        def set_categoryon_selected(evt):

            def edit_function():
                self._set_category_to_selected_events()
            safe_locking(self, edit_function)

        def measure_distance(evt):
            self._measure_distance_between_events()

        def set_category_on_without(evt):
            def edit_function():
                self._set_category()
            safe_locking(self, edit_function)

        def edit_eras(evt):
            def edit_function():
                self._edit_eras()
            safe_locking(self, edit_function)

        def set_readonly(evt):
            self.controller.set_timeline_in_readonly_mode()

        def undo(evt):
            safe_locking(self, self.timeline.undo)

        def redo(evt):
            safe_locking(self, self.timeline.redo)

        def compress(evt):
            safe_locking(self, self.timeline.compress)

        def move_up_handler(event):
            self.main_panel.timeline_panel.move_selected_event_up()

        def move_down_handler(event):
            self.main_panel.timeline_panel.move_selected_event_down()

        cbx = NONE
        items_spec = ((ID_CREATE_EVENT, create_event, _("Create &Event..."), cbx),
                      (ID_EDIT_EVENT, edit_event, _("&Edit Selected Event..."), cbx),
                      (ID_DUPLICATE_EVENT, duplicate_event, _("&Duplicate Selected Event..."), cbx),
                      (ID_SET_CATEGORY_ON_SELECTED, set_categoryon_selected, _("Set Category on Selected Events..."), cbx),
                      (ID_MOVE_EVENT_UP, move_up_handler, _("Move event up") + "\tAlt+Up", cbx),
                      (ID_MOVE_EVENT_DOWN, move_down_handler, _("Move event down") + "\tAlt+Down", cbx),
                      None,
                      (ID_CREATE_MILESTONE, create_milestone, _("Create &Milestone..."), cbx),
                      None,
                      (ID_COMPRESS, compress, _("&Compress timeline Events"), cbx),
                      None,
                      (ID_MEASURE_DISTANCE, measure_distance, _("&Measure Distance between two Events..."), cbx),
                      None,
                      (ID_SET_CATEGORY_ON_WITHOUT, set_category_on_without,
                       _("Set Category on events &without category..."), cbx),
                      None,
                      (ID_EDIT_ERAS, edit_eras, _("Edit Era's..."), cbx),
                      None,
                      (ID_SET_READONLY, set_readonly, _("&Read Only"), cbx),
                      None,
                      (ID_UNDO, undo, _("&Undo") + "\tCtrl+Z", cbx),
                      (ID_REDO, redo, _("&Redo") + "\tAlt+Z", cbx))
        self._timeline_menu = self._create_menu(items_spec)
        self._add_timeline_menu_items_to_controller(self._timeline_menu)
        return self._timeline_menu

    def _add_timeline_menu_items_to_controller(self, menu):
        self._add_to_controller_requiring_writeable_timeline(menu, ID_CREATE_EVENT)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_EDIT_EVENT)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_CREATE_MILESTONE)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_DUPLICATE_EVENT)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_SET_CATEGORY_ON_SELECTED)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_MEASURE_DISTANCE)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_SET_CATEGORY_ON_WITHOUT)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_SET_READONLY)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_EDIT_ERAS)
        self._add_to_controller_requiring_writeable_timeline(menu, ID_COMPRESS)

    def _add_to_controller_requiring_writeable_timeline(self, menu, item_id):
        mnu_item = menu.FindItemById(item_id)
        self.menu_controller.add_menu_requiring_writable_timeline(mnu_item)

    def _create_navigate_menu(self):

        def find_first(evt):
            event = self.timeline.get_first_event()
            if event:
                start = event.get_start_time()
                delta = self.main_panel.get_displayed_period_delta()
                end = start + delta
                margin_delta = delta / 24
                self.main_panel.Navigate(lambda tp: tp.update(start, end, -margin_delta))

        def find_last(evt):
            event = self.timeline.get_last_event()
            if event:
                end = event.get_end_time()
                delta = self.main_panel.get_displayed_period_delta()
                try:
                    start = end - delta
                except ValueError:
                    start = self.timeline.get_time_type().get_min_time()
                margin_delta = delta / 24
                self.main_panel.Navigate(lambda tp: tp.update(start, end, end_delta=margin_delta))

        def restore_time_period(evt):
            if self.prev_time_period:
                self.main_panel.Navigate(lambda tp: self.prev_time_period)

        def fit_all(evt):
            self._fit_all_events()

        cbx = NONE
        items_spec = (None,
                      (ID_FIND_FIRST, find_first, _("Find &First Event"), cbx),
                      (ID_FIND_LAST, find_last, _("Find &Last Event"), cbx),
                      (ID_FIT_ALL, fit_all, _("Fit &All Events"), cbx),
                      None,
                      (ID_RESTORE_TIME_PERIOD, restore_time_period, _("Go to previous time period"), cbx),)
        self._navigation_menu_items = []
        self._navigation_functions_by_menu_item_id = {}
        self.update_navigation_menu_items()
        self._navigate_menu = self._create_menu(items_spec)
        self._add_navigate_menu_items_to_controller(self._navigate_menu)
        return self._navigate_menu

    def _add_navigate_menu_items_to_controller(self, menu):
        menu_ids = (ID_FIND_FIRST, ID_FIND_LAST, ID_FIT_ALL, ID_RESTORE_TIME_PERIOD)
        for menu_id in menu_ids:
            self._add_to_controller_requiring_timeline(menu, menu_id)

    def _add_to_controller_requiring_timeline(self, menu, item_id):
        mnu_item = menu.FindItemById(item_id)
        self.menu_controller.add_menu_requiring_timeline(mnu_item)

    def _create_menu(self, items_spec):
        menu = wx.Menu()
        for item in items_spec:
            if item is not None:
                self._create_menu_item(menu, item)
            else:
                menu.AppendSeparator()
        return menu

    def _create_menu_item(self, menu, item_spec):
        if isinstance(item_spec, collections.Callable):
            item_spec(menu)
        else:
            item_id, handler, label, checkbox = item_spec
            if label is not None:
                if checkbox == CHECKBOX:
                    item = menu.Append(item_id, label, kind=wx.ITEM_CHECK)
                elif checkbox == CHECKED_RB:
                    item = menu.Append(item_id, label, kind=wx.ITEM_RADIO)
                    item.Check(True)
                elif checkbox == UNCHECKED_RB:
                    item = menu.Append(item_id, label, kind=wx.ITEM_RADIO)
                else:
                    if label is not None:
                        item = menu.Append(item_id, label)
                    else:
                        item = menu.Append(item_id)
            else:
                item = menu.Append(item_id)
            self.shortcut_items[item_id] = menu.FindItemById(item_id)
            self.Bind(wx.EVT_MENU, handler, item)

    def _mnu_file_new_on_click(self, event):
        items = [
            {
                "text": _("Gregorian"),
                "description": _("This creates a timeline using the standard calendar."),
                "create_fn": self._create_new_timeline,
            },
            {
                "text": _("Numeric"),
                "description": _("This creates a timeline that has numbers on the x-axis instead of dates."),
                "create_fn": self._create_new_numeric_timeline,
            },
            {
                "text": _("Directory"),
                "description": _("This creates a timeline where the modification date of files in a directory are shown as events."),
                "create_fn": self._create_new_dir_timeline,
            },
            {
                "text": _("Bosparanian"),
                "description": _("This creates a timeline using the fictuous Bosparanian calendar from the German pen-and-paper RPG \"The Dark Eye\" (\"Das schwarze Auge\", DSA)."),
                "create_fn": self._create_new_bosparanian_timeline,
            },
            {
                "text": _("Pharaonic"),
                "description": _("This creates a timeline using the ancient egypt pharaonic calendar"),
                "create_fn": self._create_new_pharaonic_timeline,
            },
            {
                "text": _("Coptic"),
                "description": _("This creates a timeline using the coptic calendar"),
                "create_fn": self._create_new_coptic_timeline,
            },
        ]
        dialog = FileNewDialog(self, items)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.GetSelection()["create_fn"]()
        dialog.Destroy()

    def _mnu_file_open_on_click(self, event):
        self._open_existing_timeline()

    def mnu_file_save_as_on_click(self, event):
        if self.timeline is not None:
            self._save_as()

    def _mnu_file_import_on_click(self, menu):
        def open_import_dialog():
            dialog = ImportEventsDialog(self.timeline, self)
            dialog.ShowModal()
            dialog.Destroy()
        safe_locking(self, open_import_dialog)

    def _mnu_file_exit_on_click(self, evt):
        self.Close()

    def _add_ellipses_to_menuitem(self, wx_id):
        plain = wx.GetStockLabel(wx_id, wx.STOCK_WITH_ACCELERATOR | wx.STOCK_WITH_MNEMONIC)
        # format of plain 'xxx[\tyyy]', example '&New\tCtrl+N'
        tab_index = plain.find("\t")
        if tab_index != -1:
            return plain[:tab_index] + "..." + plain[tab_index:]
        return plain + "..."
