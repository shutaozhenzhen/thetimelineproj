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
REQUIRING_VISIBLE_TIMELINE_VIEW = (mid.ID_SIDEBAR,)


class ViewMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_TOOLBAR: lambda evt: parent.config.set('show_toolbar', evt.IsChecked()),
            mid.ID_SIDEBAR: lambda evt: parent.config.set('show_sidebar', evt.IsChecked()),
            mid.ID_LEGEND: lambda evt: parent.config.set('show_legend', evt.IsChecked()),
            mid.ID_BALLOONS: lambda evt: parent.config.set('balloon_on_hover', evt.IsChecked()),
            mid.ID_ZOOMIN: lambda evt: DrawingAreaProxy(parent).zoom_in(),
            mid.ID_ZOOMOUT: lambda evt: DrawingAreaProxy(parent).zoom_out(),
            mid.ID_VERT_ZOOMIN: lambda evt: DrawingAreaProxy(parent).vertical_zoom_in(),
            mid.ID_VERT_ZOOMOUT: lambda evt: DrawingAreaProxy(parent).vertical_zoom_out(),
            mid.ID_PRESENTATION: lambda evt: parent.start_slide_show(),
            mid.ID_HIDE_DONE: lambda evt: parent.config.set('hide_events_done', evt.IsChecked()),
            mid.ID_LEFT_ALIGNMENT: lambda evt: parent.config.set('draw_point_events_to_right', True),
            mid.ID_CENTER_ALIGNMENT: lambda evt: parent.config.set('draw_point_events_to_right', False),
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE, REQUIRING_VISIBLE_TIMELINE_VIEW)
        self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts()
        self._register_menus_requiring_timeline()
        self._check_view_menu_items()

    def _create_menu(self):
        self.Append(mid.ID_TOOLBAR, _("Toolbar"), kind=wx.ITEM_CHECK)
        self.Append(mid.ID_SIDEBAR, _("&Sidebar") + "\tCtrl+I", kind=wx.ITEM_CHECK)
        self.Append(mid.ID_LEGEND, _("&Legend"), kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.Append(mid.ID_BALLOONS, _("&Balloons on hover"), kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.Append(mid.ID_ZOOMIN, _("Zoom &In") + "\tCtrl++")
        self.Append(mid.ID_ZOOMOUT, _("Zoom &Out") + "\tCtrl+-")
        self.Append(mid.ID_VERT_ZOOMIN, _("Vertical Zoom &In") + "\tAlt++")
        self.Append(mid.ID_VERT_ZOOMOUT, _("Vertical Zoom &Out") + "\tAlt+-")
        self.AppendSeparator()
        point_even_alignmentsub_menu = wx.Menu()
        point_even_alignmentsub_menu.Append(mid.ID_LEFT_ALIGNMENT, _("Left"), kind=wx.ITEM_RADIO)
        point_even_alignmentsub_menu.Append(mid.ID_CENTER_ALIGNMENT, _("Center"), kind=wx.ITEM_RADIO)
        self.Append(wx.ID_ANY, _("Point event alignment"), point_even_alignmentsub_menu)
        self.AppendSeparator()
        self.Append(wx.ID_ANY, _("Event appearance"), self._create_event_box_drawers_submenu())
        self.AppendSeparator()
        self.Append(mid.ID_PRESENTATION, _("Start slide show") + "...")
        self.AppendSeparator()
        self.Append(mid.ID_HIDE_DONE, _("&Hide Events done"), kind=wx.ITEM_CHECK)

    def _check_view_menu_items(self):
        self.FindItemById(mid.ID_TOOLBAR).Check(self._parent.config.show_toolbar)
        self.FindItemById(mid.ID_SIDEBAR).Check(self._parent.config.show_sidebar)
        self.FindItemById(mid.ID_LEGEND).Check(self._parent.config.show_legend)
        self.FindItemById(mid.ID_BALLOONS).Check(self._parent.config.balloon_on_hover)
        self.FindItemById(mid.ID_HIDE_DONE).Check(self._parent.config.hide_events_done)
        self.FindItemById(mid.ID_LEFT_ALIGNMENT).Check(self._parent.config.draw_point_events_to_right)
        self.FindItemById(mid.ID_CENTER_ALIGNMENT).Check(not self._parent.config.draw_point_events_to_right)

    def _create_event_box_drawers_submenu(self):
        submenu = wx.Menu()
        for plugin in factory.get_plugins(EVENTBOX_DRAWER):
            self.create_submenu(plugin, submenu)
        return submenu

    def create_submenu(self, plugin, submenu):
        wxid = plugin.wxid()
        submenu.Append(wxid, plugin.display_name(), plugin.display_name(), kind=wx.ITEM_RADIO)
        self._parent.Bind(wx.EVT_MENU, self._plugin_handler(plugin), id=wxid)
        self._parent.menu_controller.add_menu_requiring_timeline(submenu.FindItemById(wxid))
        self._parent.shortcut_items[wxid] = submenu.FindItemById(wxid)
        if plugin.display_name() == self._parent.config.get_selected_event_box_drawer():
            submenu.FindItemById(wxid).Check()

    def _plugin_handler(self, plugin):
        def event_handler(evt):
            self._parent.main_panel.get_timeline_canvas().SetEventBoxDrawer(plugin.run())
            self._parent.config.set_selected_event_box_drawer(plugin.display_name())
        return event_handler
