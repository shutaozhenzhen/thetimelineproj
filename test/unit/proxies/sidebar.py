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


import unittest
from mock import Mock
from timelinelib.proxies.sidebar import SidebarProxy
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.wxgui.components.mainpanel import MainPanel
from timelinelib.wxgui.components.timelinepanel import TimelinePanel
from timelinelib.wxgui.components.sidebar import Sidebar
from timelinelib.wxgui.components.sidebar import CustomCategoryTree


class describe_sidebar_proxy(unittest.TestCase):
    
    def test_canvas_check_categories_called(self):
        self.proxy.check_categories(self.categories)
        self.catecory_tree.check_categories.assert_called_once_with(self.categories)
    
    def test_canvas_uncheck_categories_called(self):
        self.proxy.uncheck_categories(self.categories)
        self.catecory_tree.uncheck_categories.assert_called_once_with(self.categories)
    
    def setUp(self):
        self.categories = []
        self.catecory_tree = Mock(CustomCategoryTree)
        self.proxy = SidebarProxy(self.create_mainframe_object())
        
    def create_mainframe_object(self):
        mf = Mock(MainFrame)
        mf.main_panel = Mock(MainPanel)
        mf.main_panel.timeline_panel = Mock(TimelinePanel)
        mf.main_panel.timeline_panel.sidebar = Mock(Sidebar)
        mf.main_panel.timeline_panel.sidebar.category_tree = self.catecory_tree
        return mf
        