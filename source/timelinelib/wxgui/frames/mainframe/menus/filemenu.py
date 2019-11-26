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

import wx
from timelinelib.db.utils import safe_locking
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.plugin.factory import EXPORTER
from timelinelib.plugin import factory
from timelinelib.wxgui.dialogs.filenew.view import FileNewDialog
from timelinelib.wxgui.dialogs.importevents.view import ImportEventsDialog

ID_IMPORT = wx.NewId()

SHORTCUTS = (wx.ID_NEW, wx.ID_SAVEAS, ID_IMPORT, wx.ID_EXIT)
REQUIRING_TIMELINE = (ID_IMPORT, wx.ID_SAVEAS)


class FileMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            wx.ID_NEW: self._new,
            wx.ID_OPEN: self._open,
            wx.ID_SAVEAS: self._save_as,
            ID_IMPORT: self._import,
            wx.ID_EXIT: self._exit,
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)

    def create(self):
        menu = self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts(menu)
        self._register_menus_requiring_timeline(menu)
        return menu

    def _create_menu(self):
        menu = wx.Menu()
        self._create_new_menu_item(menu)
        menu.Append(wx.ID_OPEN, self.add_ellipses_to_menuitem(wx.ID_OPEN), _("Open an existing timeline"))
        self._create_open_recent_menu(menu)
        menu.AppendSeparator()
        menu.Append(wx.ID_SAVEAS, "", _("Save As..."))
        menu.AppendSeparator()
        menu.Append(ID_IMPORT, _("Import events..."), _("Import events..."))
        menu.AppendSeparator()
        self._create_export_menues(menu)
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "", _("Exit the program"))
        return menu

    @staticmethod
    def _create_new_menu_item(file_menu):
        accel = wx.GetStockLabel(wx.ID_NEW, wx.STOCK_WITH_ACCELERATOR | wx.STOCK_WITH_MNEMONIC)
        accel = accel.split("\t", 1)[1]
        file_menu.Append(wx.ID_NEW, _("New...") + "\t" + accel, _("Create a new timeline"))

    def _create_open_recent_menu(self, file_menu):
        self._parent.mnu_file_open_recent_submenu = wx.Menu()
        file_menu.Append(wx.ID_ANY, _("Open &Recent"), self._parent.mnu_file_open_recent_submenu)
        self._parent.update_open_recent_submenu()

    def _create_export_menues(self, file_menu):

        def create_click_handler(plugin, main_frame):
            def event_handler(evt):
                plugin.run(main_frame)
            return event_handler

        submenu = wx.Menu()
        file_menu.Append(wx.ID_ANY, _("Export"), submenu)
        for plugin in factory.get_plugins(EXPORTER):
            mnu = submenu.Append(wx.ID_ANY, plugin.display_name(), plugin.display_name())
            self._parent.menu_controller.add_menu_requiring_timeline(mnu)
            handler = create_click_handler(plugin, self)
            self._parent.Bind(wx.EVT_MENU, handler, mnu)
            method = getattr(plugin, "wxid", None)
            if callable(method):
                self._parent.shortcut_items[method()] = mnu

    def _new(self, evt):
        items = [
            {
                "text": _("Gregorian"),
                "description": _("This creates a timeline using the standard calendar."),
                "create_fn": self._parent._create_new_timeline,
            },
            {
                "text": _("Numeric"),
                "description": _("This creates a timeline that has numbers on the x-axis instead of dates."),
                "create_fn": self._parent._create_new_numeric_timeline,
            },
            {
                "text": _("Directory"),
                "description": _("This creates a timeline where the modification date of files in a directory are shown as events."),
                "create_fn": self._parent._create_new_dir_timeline,
            },
            {
                "text": _("Bosparanian"),
                "description": _("This creates a timeline using the fictuous Bosparanian calendar from the German pen-and-paper RPG \"The Dark Eye\" (\"Das schwarze Auge\", DSA)."),
                "create_fn": self._parent._create_new_bosparanian_timeline,
            },
            {
                "text": _("Pharaonic"),
                "description": _("This creates a timeline using the ancient egypt pharaonic calendar"),
                "create_fn": self._parent._create_new_pharaonic_timeline,
            },
            {
                "text": _("Coptic"),
                "description": _("This creates a timeline using the coptic calendar"),
                "create_fn": self._parent._create_new_coptic_timeline,
            },
        ]
        dialog = FileNewDialog(self._parent, items)
        if dialog.ShowModal() == wx.ID_OK:
            dialog.GetSelection()["create_fn"]()
        dialog.Destroy()

    def _open(self, evt):
        self._parent._open_existing_timeline()

    def _save_as(self, evt):
        if self._parent.timeline is not None:
            self._parent._save_as()

    def _import(self, evt):
        def open_import_dialog():
            dialog = ImportEventsDialog(self._parent.timeline, self._parent)
            dialog.ShowModal()
            dialog.Destroy()
        safe_locking(self._parent, open_import_dialog)

    def _exit(self, evt):
        self._parent.Close()
