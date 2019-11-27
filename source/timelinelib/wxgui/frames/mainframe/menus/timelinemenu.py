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
from timelinelib.wxgui.dialogs.editevent.view import open_create_event_editor
from timelinelib.wxgui.dialogs.milestone.view import open_milestone_editor_for
from timelinelib.db.utils import safe_locking


SHORTCUTS = list()
REQUIRING_TIMELINE = list()
REQUIRING_WRITEABLE_TIMELINE = (mid.ID_CREATE_EVENT, mid.ID_EDIT_EVENT, mid.ID_CREATE_MILESTONE, mid.ID_DUPLICATE_EVENT,
                                mid.ID_SET_CATEGORY_ON_SELECTED, mid.ID_MOVE_EVENT_UP, mid.ID_MOVE_EVENT_DOWN,
                                mid.ID_MEASURE_DISTANCE, mid.ID_SET_CATEGORY_ON_WITHOUT,
                                mid.ID_SET_READONLY, mid.ID_EDIT_ERAS, mid.ID_COMPRESS, mid.ID_UNDO, mid.ID_REDO)


class TimelineMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_CREATE_EVENT: lambda evt: open_create_event_editor(parent, parent, parent.config, parent.timeline),
            mid.ID_EDIT_EVENT: lambda evt: parent.edit_event(),
            mid.ID_DUPLICATE_EVENT: lambda evt: parent.duplicate_event(),
            mid.ID_SET_CATEGORY_ON_SELECTED: lambda evt: parent.set_category_on_selected(),
            mid.ID_MOVE_EVENT_UP: lambda evt: parent.move_selected_event_up(),
            mid.ID_MOVE_EVENT_DOWN: lambda evt: parent.move_selected_event_down(),
            mid.ID_CREATE_MILESTONE: lambda evt: open_milestone_editor_for(parent, parent, parent.config, parent.timeline),
            mid.ID_COMPRESS: lambda evt: safe_locking(parent, parent.timeline.compress),
            mid.ID_MEASURE_DISTANCE: lambda evt: parent.measure_distance_between_events(),
            mid.ID_SET_CATEGORY_ON_WITHOUT: lambda evt: safe_locking(self._parent, lambda: parent.set_category()),
            mid.ID_EDIT_ERAS: lambda evt: safe_locking(parent, lambda: parent.edit_eras()),
            mid.ID_SET_READONLY: lambda evt: self._parent.set_readonly_mode(),
            mid.ID_UNDO: lambda evt: safe_locking(parent, parent.timeline.undo),
            mid.ID_REDO: lambda evt: safe_locking(parent, parent.timeline.redo),
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE,
                          requiring_writeable_timeline=REQUIRING_WRITEABLE_TIMELINE)

    def create(self):
        menu = self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts(menu)
        self._register_menus_requiring_timeline(menu)
        return menu

    def _create_menu(self):
        menu = wx.Menu()
        menu.Append(mid.ID_CREATE_EVENT, _("Create &Event..."))
        menu.Append(mid.ID_EDIT_EVENT, _("&Edit Selected Event..."))
        menu.Append(mid.ID_DUPLICATE_EVENT, _("&Duplicate Selected Event..."))
        menu.Append(mid.ID_SET_CATEGORY_ON_SELECTED, _("Set Category on Selected Events..."))
        menu.Append(mid.ID_MOVE_EVENT_UP, _("Move event up") + "\tAlt+Up")
        menu.Append(mid.ID_MOVE_EVENT_DOWN, _("Move event down") + "\tAlt+Down")
        menu.AppendSeparator()
        menu.Append(mid.ID_CREATE_MILESTONE, _("Create &Milestone..."))
        menu.AppendSeparator()
        menu.Append(mid.ID_COMPRESS, _("&Compress timeline Events"))
        menu.AppendSeparator()
        menu.Append(mid.ID_MEASURE_DISTANCE, _("&Measure Distance between two Events..."))
        menu.AppendSeparator()
        menu.Append(mid.ID_SET_CATEGORY_ON_WITHOUT, _("Set Category on events &without category..."))
        menu.AppendSeparator()
        menu.Append(mid.ID_EDIT_ERAS, _("Edit Era's..."))
        menu.AppendSeparator()
        menu.Append(mid.ID_SET_READONLY, _("&Read Only"))
        menu.AppendSeparator()
        menu.Append(mid.ID_UNDO, _("&Undo") + "\tCtrl+Z")
        menu.Append(mid.ID_REDO, _("&Redo") + "\tAlt+Z")
        return menu
