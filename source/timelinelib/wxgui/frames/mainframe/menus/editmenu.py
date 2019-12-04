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
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.wxgui.dialogs.preferences.view import open_preferences_dialog
from timelinelib.wxgui.dialogs.shortcutseditor.view import open_shortcuts_editor_dialog
from timelinelib.wxgui.dialogs.categoryfinder.view import open_category_finder_dialog
from timelinelib.wxgui.dialogs.milestonefinder.view import open_milestone_finder_dialog

SHORTCUTS = (mid.ID_FIND, mid.ID_FIND_MILESTONES, mid.ID_SELECT_ALL, mid.ID_PREFERENCES, mid.ID_EDIT_SHORTCUTS)
REQUIRING_TIMELINE = (mid.ID_FIND, mid.ID_FIND_CATEGORIES, mid.ID_FIND_MILESTONES, mid.ID_SELECT_ALL)


class EditMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_FIND: lambda evt: parent.main_panel.show_searchbar(True),
            mid.ID_FIND_CATEGORIES: lambda evt: open_category_finder_dialog(parent, parent.timeline),
            mid.ID_FIND_MILESTONES: lambda evt: open_milestone_finder_dialog(parent, parent.timeline),
            mid.ID_SELECT_ALL: lambda evt: parent.controller.select_all(),
            mid.ID_PREFERENCES: lambda evt: open_preferences_dialog(parent, parent.config),
            mid.ID_EDIT_SHORTCUTS: lambda evt: open_shortcuts_editor_dialog(parent, parent.shortcut_controller),
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)
        self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts()
        self._register_menus_requiring_timeline()

    def _create_menu(self):
        self.Append(mid.ID_FIND)
        self.Append(mid.ID_FIND_CATEGORIES, _("Find Categories..."))
        self.Append(mid.ID_FIND_MILESTONES, _("Find Milestones..."))
        self.AppendSeparator()
        self.Append(mid.ID_SELECT_ALL, _("Select All Events"))
        self.AppendSeparator()
        self.Append(mid.ID_PREFERENCES)
        self.Append(mid.ID_EDIT_SHORTCUTS, _("Shortcuts..."))
