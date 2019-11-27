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
from timelinelib.plugin.factory import EVENTBOX_DRAWER
from timelinelib.plugin import factory
from timelinelib.proxies.drawingarea import DrawingAreaProxy


SHORTCUTS = (mid.ID_SIDEBAR, mid.ID_LEGEND, mid.ID_BALLOONS, mid.ID_ZOOMIN, mid.ID_ZOOMOUT, mid.ID_VERT_ZOOMIN,
             mid.ID_VERT_ZOOMOUT, mid.ID_PRESENTATION)
REQUIRING_TIMELINE = (mid.ID_LEGEND, mid.ID_BALLOONS, mid.ID_ZOOMIN, mid.ID_ZOOMOUT, mid.ID_VERT_ZOOMIN,
                      mid.ID_VERT_ZOOMOUT, mid.ID_PRESENTATION)
REQUIRING_VISIBLE_TIMELINE_VIEW = (mid.ID_SIDEBAR, )


class ViewMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_TOOLBAR: lambda evt: parent.config.set('show_toolbar', evt.IsChecked()),
            mid.ID_SIDEBAR: lambda evt: parent.config.set('show_sidebar', evt.IsChecked()),
            mid.ID_LEGEND: lambda evt: parent.config.set('show_legend', evt.IsChecked()),
            mid.ID_BALLOONS: lambda evt: parent.config.set('balloon_on_hover', evt.IsChecked()),
            mid.ID_ZOOMIN: self._zoomoin,
            mid.ID_ZOOMOUT: self._zoomout,
            mid.ID_VERT_ZOOMIN: self._vert_zoomoin,
            mid.ID_VERT_ZOOMOUT: self._vert_zoomout,
            mid.ID_PRESENTATION: self.start_slide_show,
            mid.ID_HIDE_DONE: lambda evt: parent.config.set('hide_events_done', evt.IsChecked()),
            mid.ID_LEFT_ALIGNMENT: lambda evt: parent.config.set('draw_point_events_to_right', True),
            mid.ID_CENTER_ALIGNMENT: lambda evt: parent.config.set('draw_point_events_to_right', False),
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
        menu.Append(mid.ID_TOOLBAR, _("Toolbar"), kind=wx.ITEM_CHECK)
        menu.Append(mid.ID_SIDEBAR, _("&Sidebar") + "\tCtrl+I", kind=wx.ITEM_CHECK)
        menu.Append(mid.ID_LEGEND, _("&Legend"), kind=wx.ITEM_CHECK)
        menu.AppendSeparator()
        menu.Append(mid.ID_BALLOONS, _("&Balloons on hover"), kind=wx.ITEM_CHECK)
        menu.AppendSeparator()
        menu.Append(mid.ID_ZOOMIN, _("Zoom &In") + "\tCtrl++")
        menu.Append(mid.ID_ZOOMOUT, _("Zoom &Out") + "\tCtrl+-")
        menu.Append(mid.ID_VERT_ZOOMIN, _("Vertical Zoom &In") + "\tAlt++")
        menu.Append(mid.ID_VERT_ZOOMOUT, _("Vertical Zoom &Out") + "\tAlt+-")
        menu.AppendSeparator()
        self._create_point_event_alignment_submenu(menu)
        menu.AppendSeparator()
        self._create_event_box_drawers_submenu(menu)
        menu.AppendSeparator()
        menu.Append(mid.ID_PRESENTATION, _("Start slide show") + "...")
        menu.AppendSeparator()
        menu.Append(mid.ID_HIDE_DONE, _("&Hide Events done"), kind=wx.ITEM_CHECK)
        return menu

    def _check_view_menu_items(self, menu):
        menu.FindItemById(mid.ID_TOOLBAR).Check(self._parent.config.show_toolbar)
        menu.FindItemById(mid.ID_SIDEBAR).Check(self._parent.config.show_sidebar)
        menu.FindItemById(mid.ID_LEGEND).Check(self._parent.config.show_legend)
        menu.FindItemById(mid.ID_BALLOONS).Check(self._parent.config.balloon_on_hover)
        menu.FindItemById(mid.ID_HIDE_DONE).Check(self._parent.config.hide_events_done)
        menu.FindItemById(mid.ID_LEFT_ALIGNMENT).Check(self._parent.config.draw_point_events_to_right)
        menu.FindItemById(mid.ID_CENTER_ALIGNMENT).Check(not self._parent.config.draw_point_events_to_right)

    def _create_point_event_alignment_submenu(self, menu):
        sub_menu = wx.Menu()
        sub_menu.Append(mid.ID_LEFT_ALIGNMENT, _("Left"), kind=wx.ITEM_RADIO)
        sub_menu.Append(mid.ID_CENTER_ALIGNMENT, _("Center"), kind=wx.ITEM_RADIO)
        menu.Append(wx.ID_ANY, _("Point event alignment"), sub_menu)

    def _create_event_box_drawers_submenu(self, menu):
        sub_menu = wx.Menu()
        for plugin in factory.get_plugins(EVENTBOX_DRAWER):
            item = sub_menu.Append(wx.ID_ANY, plugin.display_name(), kind=wx.ITEM_RADIO)
            self._parent.Bind(wx.EVT_MENU, self._plugin_handler(plugin), item)
            if plugin.display_name() == self._parent.config.get_selected_event_box_drawer():
                item.Check()
        menu.Append(wx.ID_ANY, _("Event appearance"), sub_menu)

    def _plugin_handler(self, plugin):
        def event_handler(evt):
            self._parent.main_panel.get_timeline_canvas().SetEventBoxDrawer(plugin.run())
            self._parent.config.set_selected_event_box_drawer(plugin.display_name())
        return event_handler

    def _zoomoin(self, evt):
        DrawingAreaProxy(self._parent).zoom_in()

    def _zoomout(self, evt):
        DrawingAreaProxy(self._parent).zoom_out()

    def _vert_zoomoin(self, evt):
        DrawingAreaProxy(self._parent).vertical_zoom_in()

    def _vert_zoomout(self, evt):
        DrawingAreaProxy(self._parent).vertical_zoom_out()

    def start_slide_show(self, evt):
        self._parent.controller.start_slide_show()
