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


import wx

from timelinelib.canvas.timelinecanvas import TimelineCanvas
from timelinelib.utilities.observer import Listener
from timelinelib.wxgui.components.messagebar import MessageBar
from timelinelib.wxgui.components.sidebar import Sidebar
from timelinelib.wxgui.frames.mainframe.toolbar import ToolbarCreator


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
            self.status_bar_adapter,
            self.handle_db_error,
            self.config,
            self.main_frame)
        self.timeline_canvas.Bind(
            TimelineCanvas.EVT_DIVIDER_POSITION_CHANGED,
            self._timeline_canvas_on_divider_position_changed
        )
        self.timeline_canvas.Bind(
            TimelineCanvas.EVT_MOUSE_MOVED,
            self._timeline_canvas_on_mouse_moved
        )
        self.timeline_canvas.SetDividerPosition(self.config.divider_line_slider_pos)

    def _timeline_canvas_on_divider_position_changed(self, event):
        self.divider_line_slider.SetValue(self.timeline_canvas.GetDividerPosition())
        self.config.divider_line_slider_pos = self.timeline_canvas.GetDividerPosition()

    def _timeline_canvas_on_mouse_moved(self, event):
        if event.event is None:
            self.status_bar_adapter.set_text(event.time_string)
        else:
            self.status_bar_adapter.set_text(event.event.get_label())

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
        self.timeline_canvas.open_event_editor_for(event)

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
