# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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


import webbrowser

import wx

from timelinelib.canvas import EVT_DIVIDER_POSITION_CHANGED
from timelinelib.canvas import EVT_HINT
from timelinelib.canvas import EVT_TIMELINE_REDRAWN
from timelinelib.canvas.timelinecanvas import TimelineCanvas
from timelinelib.db.exceptions import TimelineIOError
from timelinelib.db.utils import safe_locking
from timelinelib.features.experimental.experimentalfeatures import EVENT_DONE
from timelinelib.features.experimental.experimentalfeatures import experimental_feature
from timelinelib.utilities.encodings import to_unicode
from timelinelib.utilities.observer import Listener
from timelinelib.wxgui.components.messagebar import MessageBar
from timelinelib.wxgui.components.sidebar import Sidebar
from timelinelib.wxgui.dialogs.duplicateevent.view import open_duplicate_event_dialog_for_event
from timelinelib.wxgui.dialogs.editevent.view import open_create_event_editor
from timelinelib.wxgui.dialogs.editevent.view import open_event_editor_for
from timelinelib.wxgui.frames.mainframe.toolbar import ToolbarCreator
from timelinelib.wxgui.utils import _ask_question


class TimelinePanelGuiCreator(wx.Panel):

    def __init__(self, parent):
        self.sidebar_width = self.config.get_sidebar_width()
        wx.Panel.__init__(self, parent)
        self._create_gui()

    def _create_gui(self):
        self._create_toolbar()
        self._create_warning_bar()
        self._create_divider_line_slider()
        self._create_splitter()
        self._layout_components()

    def _create_toolbar(self):
        self.tool_bar = ToolbarCreator(self, self.config).create()

    def _create_warning_bar(self):
        self.message_bar = MessageBar(self)

    def _create_divider_line_slider(self):

        def on_slider(evt):
            self.config.divider_line_slider_pos = evt.GetPosition()

        style = wx.SL_LEFT | wx.SL_VERTICAL
        self.divider_line_slider = wx.Slider(self, size=(20, -1), style=style)
        self.Bind(wx.EVT_SCROLL, on_slider, self.divider_line_slider)

        self.divider_line_slider.Bind(wx.EVT_SLIDER, self._slider_on_slider)
        self.divider_line_slider.Bind(wx.EVT_CONTEXT_MENU, self._slider_on_context_menu)

    def _slider_on_slider(self, evt):
        self.timeline_canvas.SetDividerPosition(self.divider_line_slider.GetValue())

    def _slider_on_context_menu(self, evt):
        menu = wx.Menu()
        menu_item = wx.MenuItem(menu, wx.NewId(), _("Center"))
        self.Bind(wx.EVT_MENU, self._context_menu_on_menu_center, id=menu_item.GetId())
        menu.AppendItem(menu_item)
        self.PopupMenu(menu)
        menu.Destroy()

    def _context_menu_on_menu_center(self, evt):
        self.timeline_canvas.SetDividerPosition(50)

    def _create_splitter(self):
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(50)
        self.Bind(
            wx.EVT_SPLITTER_SASH_POS_CHANGED,
            self._splitter_on_splitter_sash_pos_changed, self.splitter)
        self._create_sidebar()
        self._create_timeline_canvas()
        self.splitter.Initialize(self.timeline_canvas)

    def _splitter_on_splitter_sash_pos_changed(self, event):
        if self.IsShown():
            self.sidebar_width = self.splitter.GetSashPosition()

    def _create_sidebar(self):
        self.sidebar = Sidebar(self.main_frame, self.splitter, self.handle_db_error)

    def _create_timeline_canvas(self):
        self.timeline_canvas = TimelineCanvas(
            self.splitter,
            self.handle_db_error,
            self.config,
            self.main_frame)
        self.timeline_canvas.Bind(
            wx.EVT_LEFT_DCLICK,
            self._timeline_canvas_on_double_clicked
        )
        self.timeline_canvas.Bind(
            wx.EVT_RIGHT_DOWN,
            self._timeline_canvas_on_right_down
        )
        self.timeline_canvas.Bind(
            wx.EVT_KEY_DOWN,
            self._timeline_canvas_on_key_down
        )
        self.timeline_canvas.Bind(
            EVT_DIVIDER_POSITION_CHANGED,
            self._timeline_canvas_on_divider_position_changed
        )
        self.timeline_canvas.Bind(
            EVT_HINT,
            self._timeline_canvas_on_hint
        )
        self.timeline_canvas.Bind(
            EVT_TIMELINE_REDRAWN,
            self._timeline_canvas_on_timeline_redrawn
        )
        self.timeline_canvas.SetDividerPosition(self.config.divider_line_slider_pos)
        self.timeline_canvas.SetEventBoxDrawer(self._get_saved_event_box_drawer())

    def _get_saved_event_box_drawer(self):
        from timelinelib.plugin import factory
        from timelinelib.plugin.factory import EVENTBOX_DRAWER
        from timelinelib.plugin.plugins.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
        plugin = factory.get_plugin(EVENTBOX_DRAWER, self.config.selected_event_box_drawer) or DefaultEventBoxDrawer()
        return plugin.run()

    def _timeline_canvas_on_double_clicked(self, event):
        if self.timeline_canvas.GetDb().is_read_only():
            return
        (x, y) = (event.GetX(), event.GetY())
        timeline_event = self.timeline_canvas.GetEventAt(x, y)
        time = self.timeline_canvas.GetTimeAt(x)
        if timeline_event is not None:
            self.open_event_editor(timeline_event)
        else:
            open_create_event_editor(
                self.main_frame,
                self.config,
                self.timeline_canvas.GetDb(),
                self.handle_db_error,
                time,
                time)
        event.Skip()

    def _timeline_canvas_on_right_down(self, event):
        (x, y) = (event.GetX(), event.GetY())
        timeline_event = self.timeline_canvas.GetEventAt(x, y)
        if timeline_event is not None and not self.timeline_canvas.GetDb().is_read_only():
            self.timeline_canvas.SetEventSelected(timeline_event, True)
            self._display_event_context_menu()
        event.Skip()

    def _timeline_canvas_on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_DELETE:
            self._delete_selected_events()
        event.Skip()

    def _display_event_context_menu(self):
        menu_definitions = [
            (_("Delete"), self._context_menu_on_delete_event, None),
        ]
        nbr_of_selected_events = len(self.timeline_canvas.GetSelectedEvents())
        if nbr_of_selected_events == 1:
            menu_definitions.insert(0, (_("Edit"), self._context_menu_on_edit_event, None))
            menu_definitions.insert(1, (_("Duplicate..."), self._context_menu_on_duplicate_event, None))
        if EVENT_DONE.enabled():
            menu_definitions.append((EVENT_DONE.get_display_name(), self._context_menu_on_done_event, None))
        menu_definitions.append((_("Select Category..."), self._context_menu_on_select_category, None))
        if nbr_of_selected_events == 1 and self.timeline_canvas.GetSelectedEvent().has_data():
            menu_definitions.append((_("Sticky Balloon"), self._context_menu_on_sticky_balloon_event, None))
        if nbr_of_selected_events == 1:
            hyperlinks = self.timeline_canvas.GetSelectedEvent().get_data("hyperlink")
            if hyperlinks is not None:
                imp = wx.Menu()
                menuid = 0
                for hyperlink in hyperlinks.split(";"):
                    imp.Append(menuid, hyperlink)
                    menuid += 1
                menu_definitions.append((_("Goto URL"), self._context_menu_on_goto_hyperlink_event, imp))
        menu = wx.Menu()
        for menu_definition in menu_definitions:
            text, method, imp = menu_definition
            menu_item = wx.MenuItem(menu, wx.NewId(), text)
            if imp is not None:
                for menu_item in imp.GetMenuItems():
                    self.Bind(wx.EVT_MENU, method, id=menu_item.GetId())
                menu.AppendMenu(wx.ID_ANY, text, imp)
            else:
                self.Bind(wx.EVT_MENU, method, id=menu_item.GetId())
                menu.AppendItem(menu_item)
        self.PopupMenu(menu)
        menu.Destroy()

    def _context_menu_on_delete_event(self, evt):
        self._delete_selected_events()

    def _delete_selected_events(self):
        selected_events = self.timeline_canvas.GetSelectedEvents()
        number_of_selected_events = len(selected_events)
        def user_ack():
            if number_of_selected_events > 1:
                text = _("Are you sure you want to delete %d events?" %
                         number_of_selected_events)
            else:
                text = _("Are you sure you want to delete this event?")
            return _ask_question(text) == wx.YES
        def exception_handler(ex):
            if isinstance(ex, TimelineIOError):
                self.handle_db_error(ex)
            else:
                raise(ex)
        def _last_event(event):
            return event.get_id() == selected_events[-1].get_id()
        def _delete_events():
            for event in selected_events:
                self.timeline_canvas.GetDb().delete_event(event.get_id(), save=_last_event(event))
        def edit_function():
            if user_ack():
                _delete_events()
            self.timeline_canvas.ClearSelectedEvents()
        safe_locking(self.main_frame, edit_function, exception_handler)

    def _context_menu_on_edit_event(self, evt):
        self.open_event_editor(self.timeline_canvas.GetSelectedEvent())

    def _context_menu_on_duplicate_event(self, evt):
        open_duplicate_event_dialog_for_event(
            self.main_frame,
            self.timeline_canvas.GetDb(),
            self.handle_db_error,
            self.timeline_canvas.GetSelectedEvent())

    @experimental_feature(EVENT_DONE)
    def _context_menu_on_done_event(self, evt):
        def exception_handler(ex):
            if isinstance(ex, TimelineIOError):
                self.handle_db_error(ex)
            else:
                raise(ex)
        def _last_event(event):
            return event.get_id() == selected_events[-1].get_id()
        def edit_function():
            for event in selected_events:
                self.timeline_canvas.GetDb().mark_event_as_done(event.get_id(), save=_last_event(event))
            self.timeline_canvas.ClearSelectedEvents()
        selected_events = self.timeline_canvas.GetSelectedEvents()
        safe_locking(self.main_frame, edit_function, exception_handler)

    def _context_menu_on_select_category(self, evt):
        self.main_frame.set_category_on_selected()

    def _context_menu_on_sticky_balloon_event(self, evt):
        self.timeline_canvas.SetEventStickyBalloon(self.timeline_canvas.GetSelectedEvent(), True)

    def _context_menu_on_goto_hyperlink_event(self, evt):
        hyperlinks = self.timeline_canvas.GetSelectedEvent().get_data("hyperlink")
        hyperlink = hyperlinks.split(";")[evt.Id]
        webbrowser.open(to_unicode(hyperlink))

    def _timeline_canvas_on_divider_position_changed(self, event):
        self.divider_line_slider.SetValue(self.timeline_canvas.GetDividerPosition())
        self.config.divider_line_slider_pos = self.timeline_canvas.GetDividerPosition()

    def _timeline_canvas_on_hint(self, event):
        self.status_bar_adapter.set_text(event.text)

    def _timeline_canvas_on_timeline_redrawn(self, event):
        text = _("%s events hidden") % self.timeline_canvas.GetHiddenEventCount()
        self.status_bar_adapter.set_hidden_event_count_text(text)

    def _layout_components(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.splitter, proportion=1, flag=wx.EXPAND)
        hsizer.Add(self.divider_line_slider, proportion=0, flag=wx.EXPAND)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.tool_bar, proportion=0, flag=wx.EXPAND)
        vsizer.Add(self.message_bar, proportion=0, flag=wx.EXPAND)
        vsizer.Add(hsizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vsizer)


class TimelinePanel(TimelinePanelGuiCreator):

    def __init__(self, parent, config, handle_db_error, status_bar_adapter, main_frame):
        self.config = config
        self.handle_db_error = handle_db_error
        self.status_bar_adapter = status_bar_adapter
        self.main_frame = main_frame
        TimelinePanelGuiCreator.__init__(self, parent)
        self._db_listener = Listener(self._on_db_changed)

    def set_timeline(self, timeline):
        self.timeline_canvas.set_timeline(timeline)
        self._db_listener.set_observable(timeline)

    def get_timeline_canvas(self):
        return self.timeline_canvas

    def get_scene(self):
        return self.timeline_canvas.get_drawer().scene

    def get_time_period(self):
        return self.timeline_canvas.get_time_period()

    def open_event_editor(self, event):
        open_event_editor_for(
            self.main_frame,
            self.config,
            self.timeline_canvas.GetDb(),
            self.handle_db_error,
            event)

    def redraw_timeline(self):
        self.timeline_canvas.redraw_timeline()

    def navigate_timeline(self, navigation_fn):
        return self.timeline_canvas.navigate_timeline(navigation_fn)

    def get_view_properties(self):
        return self.timeline_canvas.get_view_properties()

    def get_current_image(self):
        return self.timeline_canvas.get_current_image()

    def get_sidebar_width(self):
        return self.sidebar_width

    def show_sidebar(self):
        self.splitter.SplitVertically(self.sidebar, self.timeline_canvas, self.sidebar_width)
        self.splitter.SetSashPosition(self.sidebar_width)
        self.splitter.SetMinimumPaneSize(self.sidebar.GetBestSize()[0])

    def hide_sidebar(self):
        self.splitter.Unsplit(self.sidebar)

    def activated(self):
        if self.config.get_show_sidebar():
            self.show_sidebar()

    def _on_db_changed(self, db):
        if db.is_read_only():
            header = _("This timeline is read-only.")
            body = _("To edit this timeline, save it to a new file: File -> Save As.")
            self.message_bar.ShowInformationMessage("%s\n%s" % (header, body))
        elif not db.is_saved():
            header = _("This timeline is not being saved.")
            body = _("To save this timeline, save it to a new file: File -> Save As.")
            self.message_bar.ShowWarningMessage("%s\n%s" % (header, body))
        else:
            self.message_bar.ShowNoMessage()
