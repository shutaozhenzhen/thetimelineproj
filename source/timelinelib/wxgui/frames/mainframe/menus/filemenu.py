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
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.plugin.factory import EXPORTER
from timelinelib.plugin import factory


ID_IMPORT = wx.NewId()

SHORTCUTS = (wx.ID_NEW, wx.ID_SAVEAS, ID_IMPORT, wx.ID_EXIT)
REQUIRING_TIMELINE = (ID_IMPORT, wx.ID_SAVEAS)


class FileMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            wx.ID_NEW: parent._mnu_file_new_on_click,
            wx.ID_OPEN: parent._mnu_file_open_on_click,
            wx.ID_SAVEAS: parent.mnu_file_save_as_on_click,
            ID_IMPORT: parent._mnu_file_import_on_click,
            wx.ID_EXIT: parent._mnu_file_exit_on_click,
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
        menu.Append(wx.ID_OPEN, self._parent._add_ellipses_to_menuitem(wx.ID_OPEN), _("Open an existing timeline"))
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
