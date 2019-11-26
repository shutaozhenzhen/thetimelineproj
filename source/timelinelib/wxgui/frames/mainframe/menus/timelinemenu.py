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
from timelinelib.wxgui.dialogs.editevent.view import open_create_event_editor
from timelinelib.wxgui.dialogs.duplicateevent.view import open_duplicate_event_dialog_for_event
from timelinelib.wxgui.dialogs.milestone.view import open_milestone_editor_for
from timelinelib.db.utils import safe_locking

ID_CREATE_EVENT = wx.NewId()
ID_EDIT_EVENT = wx.NewId()
ID_DUPLICATE_EVENT = wx.NewId()
ID_SET_CATEGORY_ON_SELECTED = wx.NewId()
ID_MOVE_EVENT_UP = wx.NewId()
ID_MOVE_EVENT_DOWN = wx.NewId()
ID_CREATE_MILESTONE = wx.NewId()
ID_COMPRESS = wx.NewId()
ID_MEASURE_DISTANCE = wx.NewId()
ID_SET_CATEGORY_ON_WITHOUT = wx.NewId()
ID_EDIT_ERAS = wx.NewId()
ID_SET_READONLY = wx.NewId()
ID_UNDO = wx.NewId()
ID_REDO = wx.NewId()

SHORTCUTS = list()
REQUIRING_TIMELINE = list()
REQUIRING_WRITEABLE_TIMELINE = (ID_CREATE_EVENT, ID_EDIT_EVENT, ID_CREATE_MILESTONE, ID_DUPLICATE_EVENT,
                                ID_SET_CATEGORY_ON_SELECTED, ID_MOVE_EVENT_UP, ID_MOVE_EVENT_DOWN,
                                ID_MEASURE_DISTANCE, ID_SET_CATEGORY_ON_WITHOUT,
                                ID_SET_READONLY, ID_EDIT_ERAS, ID_COMPRESS, ID_UNDO, ID_REDO)

class TimelineMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            ID_CREATE_EVENT: self._create_event,
            ID_EDIT_EVENT: self._edit_event,
            ID_DUPLICATE_EVENT: self._duplicate_event,
            ID_SET_CATEGORY_ON_SELECTED: self._set_category_on_selected,
            ID_MOVE_EVENT_UP: self._move_event_up,
            ID_MOVE_EVENT_DOWN: self._move_event_down,
            ID_CREATE_MILESTONE: self._create_milestone,
            ID_COMPRESS: self._compress,
            ID_MEASURE_DISTANCE: self._measure_distance,
            ID_SET_CATEGORY_ON_WITHOUT: self._set_category_on_without,
            ID_EDIT_ERAS: self._edit_eras,
            ID_SET_READONLY: self._set_readonly,
            ID_UNDO: self._undo,
            ID_REDO: self._redo,
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
        menu.Append(ID_CREATE_EVENT, _("Create &Event..."))
        menu.Append(ID_EDIT_EVENT, _("&Edit Selected Event..."))
        menu.Append(ID_DUPLICATE_EVENT, _("&Duplicate Selected Event..."))
        menu.Append(ID_SET_CATEGORY_ON_SELECTED, _("Set Category on Selected Events..."))
        menu.Append(ID_MOVE_EVENT_UP, _("Move event up") + "\tAlt+Up")
        menu.Append(ID_MOVE_EVENT_DOWN, _("Move event down") + "\tAlt+Down")
        menu.AppendSeparator()
        menu.Append(ID_CREATE_MILESTONE, _("Create &Milestone..."))
        menu.AppendSeparator()
        menu.Append(ID_COMPRESS, _("&Compress timeline Events"))
        menu.AppendSeparator()
        menu.Append(ID_MEASURE_DISTANCE, _("&Measure Distance between two Events..."))
        menu.AppendSeparator()
        menu.Append(ID_SET_CATEGORY_ON_WITHOUT, _("Set Category on events &without category..."))
        menu.AppendSeparator()
        menu.Append(ID_EDIT_ERAS, _("Edit Era's..."))
        menu.AppendSeparator()
        menu.Append(ID_SET_READONLY, _("&Read Only"))
        menu.AppendSeparator()
        menu.Append(ID_UNDO, _("&Undo") + "\tCtrl+Z")
        menu.Append(ID_REDO, _("&Redo") + "\tAlt+Z")
        return menu

    def _create_event(self, evt):
        open_create_event_editor(self._parent, self._parent, self._parent.config, self._parent.timeline)

    def _edit_event(self, evt):
        try:
            event = self._get_first_selected_event()
            self._parent.main_panel.open_event_editor(event)
        except IndexError:
            # No event selected so do nothing!
            pass

    def _duplicate_event(self, evt):
        try:
            event = self._get_first_selected_event()
            open_duplicate_event_dialog_for_event(self._parent, self._parent, self._parent.timeline, event)
        except IndexError:
            # No event selected so do nothing!
            pass

    def _set_category_on_selected(self, evt):
        try:
            event = self._get_first_selected_event() # Ensure that at least one event is selected
            safe_locking(self._parent, lambda: self._parent._set_category_to_selected_events())
        except IndexError:
            # No event selected so do nothing!
            pass

    def _move_event_up(self, evt):
        self._parent.main_panel.timeline_panel.move_selected_event_up()

    def _move_event_down(self, evt):
        self._parent.main_panel.timeline_panel.move_selected_event_down()

    def _create_milestone(self, evt):
        open_milestone_editor_for(self._parent, self._parent, self._parent.config, self._parent.timeline)

    def _compress(self, evt):
        safe_locking(self._parent, self._parent.timeline.compress)

    def _measure_distance(self, evt):
        self._parent._measure_distance_between_events()

    def _set_category_on_without(self, evt):
        safe_locking(self._parent, lambda: self._parent._set_category())

    def _edit_eras(self, evt):
        safe_locking(self._parent, lambda: self._parent._edit_eras())

    def _set_readonly(self, evt):
        self._parent.controller.set_timeline_in_readonly_mode()

    def _undo(self, evt):
        safe_locking(self._parent, self._parent.timeline.undo)

    def _redo(self, evt):
        safe_locking(self._parent, self._parent.timeline.redo)

    def _get_first_selected_event(self):
        event_id = self._parent.main_panel.get_id_of_first_selected_event()
        return self._parent.timeline.find_event_with_id(event_id)
