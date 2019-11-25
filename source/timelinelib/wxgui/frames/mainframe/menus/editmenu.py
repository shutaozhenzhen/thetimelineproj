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
import timelinelib.wxgui.utils as guiutils
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.wxgui.dialogs.categoryfinder.view import CategoryFinderDialog
from timelinelib.wxgui.dialogs.milestonefinder.view import MilestoneFinderDialog
from timelinelib.wxgui.dialogs.preferences.view import PreferencesDialog
from timelinelib.wxgui.dialogs.shortcutseditor.view import ShortcutsEditorDialog

ID_SELECT_ALL = wx.NewId()
ID_FIND_CATEGORIES = wx.NewId()
ID_FIND_MILESTONES = wx.NewId()
ID_EDIT_SHORTCUTS = wx.NewId()

SHORTCUTS = (wx.ID_FIND, ID_FIND_MILESTONES, ID_SELECT_ALL, wx.ID_PREFERENCES, ID_EDIT_SHORTCUTS)
REQUIRING_TIMELINE = (wx.ID_FIND, ID_FIND_CATEGORIES, ID_FIND_MILESTONES, ID_SELECT_ALL)


class EditMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            wx.ID_FIND: self._find,
            ID_FIND_CATEGORIES: self._find_categories,
            ID_FIND_MILESTONES: self._find_milestones,
            ID_SELECT_ALL: self._select_all,
            wx.ID_PREFERENCES: self._preferences,
            ID_EDIT_SHORTCUTS: self._edit_shortcuts,
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
        menu.Append(wx.ID_FIND)
        menu.Append(ID_FIND_CATEGORIES, _("Find Categories..."))
        menu.Append(ID_FIND_MILESTONES, _("Find Milestones..."))
        menu.AppendSeparator()
        menu.Append(ID_SELECT_ALL, _("Select All Events"))
        menu.AppendSeparator()
        menu.Append(wx.ID_PREFERENCES)
        menu.Append(ID_EDIT_SHORTCUTS, _("Shortcuts..."))
        return menu

    def _find(self, evt):
        self._parent.main_panel.show_searchbar(True)

    def _find_categories(self, evt):
        guiutils.show_dialog(lambda: CategoryFinderDialog(self._parent, self._parent.timeline))

    def _find_milestones(self, evt):
        guiutils.show_dialog(lambda: MilestoneFinderDialog(self._parent, self._parent.timeline))

    def _select_all(self, evt):
        self._parent.controller.select_all()

    def _preferences(self, evt):
        safe_locking(self._parent,
                     lambda: guiutils.show_dialog(lambda: PreferencesDialog(self._parent, self._parent.config)))

    def _edit_shortcuts(self, evt):
        safe_locking(self._parent,
                     lambda: guiutils.show_dialog(lambda: ShortcutsEditorDialog(self._parent,
                                                                                self._parent.shortcut_controller)))
