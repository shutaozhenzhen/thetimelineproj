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
import timelinelib.wxgui.frames.mainframe.menus as mid
from timelinelib.db.utils import safe_locking
import timelinelib.wxgui.utils as guiutils
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.wxgui.dialogs.categoryfinder.view import CategoryFinderDialog
from timelinelib.wxgui.dialogs.milestonefinder.view import MilestoneFinderDialog
from timelinelib.wxgui.dialogs.preferences.view import PreferencesDialog
from timelinelib.wxgui.dialogs.shortcutseditor.view import ShortcutsEditorDialog
from timelinelib.wxgui.dialogs.preferences.view import open_preferences_dialog
from timelinelib.wxgui.dialogs.shortcutseditor.view import open_shortcuts_editor_dialog

SHORTCUTS = (mid.ID_FIND, mid.ID_FIND_MILESTONES, mid.ID_SELECT_ALL, mid.ID_PREFERENCES, mid.ID_EDIT_SHORTCUTS)
REQUIRING_TIMELINE = (mid.ID_FIND, mid.ID_FIND_CATEGORIES, mid.ID_FIND_MILESTONES, mid.ID_SELECT_ALL)


class EditMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_FIND: lambda evt: parent.main_panel.show_searchbar(True),
            mid.ID_FIND_CATEGORIES: self._find_categories,
            mid.ID_FIND_MILESTONES: self._find_milestones,
            mid.ID_SELECT_ALL: lambda evt: parent.controller.select_all(),
            mid.ID_PREFERENCES: lambda evt: open_preferences_dialog(parent, parent.config),
            mid.ID_EDIT_SHORTCUTS: self._edit_shortcuts,
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
        menu.Append(mid.ID_FIND)
        menu.Append(mid.ID_FIND_CATEGORIES, _("Find Categories..."))
        menu.Append(mid.ID_FIND_MILESTONES, _("Find Milestones..."))
        menu.AppendSeparator()
        menu.Append(mid.ID_SELECT_ALL, _("Select All Events"))
        menu.AppendSeparator()
        menu.Append(mid.ID_PREFERENCES)
        menu.Append(mid.ID_EDIT_SHORTCUTS, _("Shortcuts..."))
        return menu

    def _find_categories(self, evt):
        guiutils.show_dialog(lambda: CategoryFinderDialog(self._parent, self._parent.timeline))

    def _find_milestones(self, evt):
        if len([milestone.text for milestone in self._parent.timeline.all_milestones]) > 0:
            guiutils.show_dialog(lambda: MilestoneFinderDialog(self._parent, self._parent.timeline))
        else:
            guiutils.display_information_message(_('Info'), _('No Milestones found'))

    def _edit_shortcuts(self, evt):
        open_shortcuts_editor_dialog(self._parent, self._parent.shortcut_controller)
