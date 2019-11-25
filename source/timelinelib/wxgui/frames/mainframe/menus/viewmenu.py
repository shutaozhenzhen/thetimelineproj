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
from timelinelib.plugin.factory import EVENTBOX_DRAWER
from timelinelib.plugin import factory
from timelinelib.proxies.drawingarea import DrawingAreaProxy

CHECKED_RB = 2
UNCHECKED_RB = 3

ID_TOOLBAR = wx.NewId()
ID_SIDEBAR = wx.NewId()
ID_LEGEND = wx.NewId()
ID_BALLOONS = wx.NewId()
ID_ZOOMIN = wx.NewId()
ID_ZOOMOUT = wx.NewId()
ID_VERT_ZOOMIN = wx.NewId()
ID_VERT_ZOOMOUT = wx.NewId()
ID_HIDE_DONE = wx.NewId()
ID_PRESENTATION = wx.NewId()

SHORTCUTS = (ID_SIDEBAR, ID_LEGEND, ID_BALLOONS, ID_ZOOMIN, ID_ZOOMOUT, ID_VERT_ZOOMIN, ID_VERT_ZOOMOUT, ID_PRESENTATION)
REQUIRING_TIMELINE = (ID_LEGEND, ID_BALLOONS, ID_ZOOMIN, ID_ZOOMOUT, ID_VERT_ZOOMIN, ID_VERT_ZOOMOUT, ID_PRESENTATION)
REQUIRING_VISIBLE_TIMELINE_VIEW = (ID_SIDEBAR, )


class ViewMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            ID_TOOLBAR: self._on_toolbar_click,
            ID_SIDEBAR: self._sidebar,
            ID_LEGEND: self._legend,
            ID_BALLOONS: self._balloons,
            ID_ZOOMIN: self._zoomoin,
            ID_ZOOMOUT: self._zoomout,
            ID_VERT_ZOOMIN: self._vert_zoomoin,
            ID_VERT_ZOOMOUT: self._vert_zoomout,
            ID_PRESENTATION: self.start_slide_show,
            ID_HIDE_DONE: self._hide_events_done,
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE, REQUIRING_VISIBLE_TIMELINE_VIEW)

    def create(self):
        menu = self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts(menu)
        self._register_menus_requiring_timeline(menu)
        self._check_view_menu_items(menu)
        return menu

    def _create_menu(self):
        menu = wx.Menu()
        menu.Append(ID_TOOLBAR, _("Toolbar"), kind=wx.ITEM_CHECK)
        menu.Append(ID_SIDEBAR, _("&Sidebar") + "\tCtrl+I", kind=wx.ITEM_CHECK)
        menu.Append(ID_LEGEND, _("&Legend"), kind=wx.ITEM_CHECK)
        menu.AppendSeparator()
        menu.Append(ID_BALLOONS, _("&Balloons on hover"), kind=wx.ITEM_CHECK)
        menu.AppendSeparator()
        menu.Append(ID_ZOOMIN, _("Zoom &In") + "\tCtrl++")
        menu.Append(ID_ZOOMOUT, _("Zoom &Out") + "\tCtrl+-")
        menu.Append(ID_VERT_ZOOMIN, _("Vertical Zoom &In") + "\tAlt++")
        menu.Append(ID_VERT_ZOOMOUT, _("Vertical Zoom &Out") + "\tAlt+-")
        menu.AppendSeparator()
        self._create_view_point_event_alignment_menu(menu)
        menu.AppendSeparator()
        self._create_event_box_drawers_menu(menu)
        menu.AppendSeparator()
        menu.Append(ID_PRESENTATION, _("Start slide show") + "...")
        menu.AppendSeparator()
        menu.Append(ID_HIDE_DONE, _("&Hide Events done"), kind=wx.ITEM_CHECK)
        return menu

    def _check_view_menu_items(self, menu):
        menu.FindItemById(ID_TOOLBAR).Check(self._parent.config.show_toolbar)
        menu.FindItemById(ID_SIDEBAR).Check(self._parent.config.show_sidebar)
        menu.FindItemById(ID_LEGEND).Check(self._parent.config.show_legend)
        menu.FindItemById(ID_BALLOONS).Check(self._parent.config.balloon_on_hover)
        menu.FindItemById(ID_HIDE_DONE).Check(self._parent.config.hide_events_done)

    def _on_toolbar_click(self, event):
        self._parent.config.show_toolbar = event.IsChecked()

    def _create_view_point_event_alignment_menu(self, menu):
        sub_menu = wx.Menu()
        left_item = sub_menu.Append(wx.ID_ANY, _("Left"), kind=wx.ITEM_RADIO)
        center_item = sub_menu.Append(wx.ID_ANY, _("Center"), kind=wx.ITEM_RADIO)
        menu.Append(wx.ID_ANY, _("Point event alignment"), sub_menu)

        def on_first_tool_click(event):
            self._parent.config.draw_point_events_to_right = True

        def on_second_tool_click(event):
            self._parent.config.draw_point_events_to_right = False

        def check_item_corresponding_to_config():
            if self._parent.config.draw_point_events_to_right:
                left_item.Check()
            else:
                center_item.Check()

        self._parent.Bind(wx.EVT_MENU, on_first_tool_click, left_item)
        self._parent.Bind(wx.EVT_MENU, on_second_tool_click, center_item)
        self._parent.config.listen_for_any(check_item_corresponding_to_config)
        check_item_corresponding_to_config()

    def _create_event_box_drawers_menu(self, menu):

        def create_click_handler(plugin):
            def event_handler(evt):
                self._parent.main_panel.get_timeline_canvas().SetEventBoxDrawer(plugin.run())
                self._parent.config.set_selected_event_box_drawer(plugin.display_name())
            return event_handler

        items = []
        for plugin in factory.get_plugins(EVENTBOX_DRAWER):
            if plugin.display_name() == self._parent.config.get_selected_event_box_drawer():
                items.append((wx.ID_ANY, create_click_handler(plugin), plugin.display_name(), CHECKED_RB))
            else:
                items.append((wx.ID_ANY, create_click_handler(plugin), plugin.display_name(), UNCHECKED_RB))
        sub_menu = self._parent._create_menu(items)
        menu.Append(wx.ID_ANY, _("Event appearance"), sub_menu)

    def _legend(self, evt):
        self._parent.config.show_legend = evt.IsChecked()

    def _sidebar(self, evt):
        self._parent.config.show_sidebar = evt.IsChecked()
        if evt.IsChecked():
            self._parent.main_panel.show_sidebar()
        else:
            self._parent.main_panel.hide_sidebar()

    def _balloons(self, evt):
        self._parent.config.balloon_on_hover = evt.IsChecked()

    def _zoomoin(self, evt):
        DrawingAreaProxy(self._parent).zoom_in()

    def _zoomout(self, evt):
        DrawingAreaProxy(self._parent).zoom_out()

    def _vert_zoomoin(self, evt):
        DrawingAreaProxy(self._parent).vertical_zoom_in()

    def _vert_zoomout(self, evt):
        DrawingAreaProxy(self._parent).vertical_zoom_out()

    def start_slide_show(self, evt):
        canvas = self._parent.main_panel.get_timeline_canvas()
        self._parent.controller.start_slide_show(canvas)

    def _hide_events_done(self, evt):
        self._parent.config.hide_events_done = evt.IsChecked()



