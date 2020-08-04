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
from unittest.mock import Mock
from timelinelib.proxies.drawingarea import DrawingAreaProxy
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.wxgui.components.mainpanel import MainPanel
from timelinelib.wxgui.components.timelinepanel import TimelinePanel
from timelinelib.canvas import TimelineCanvas


class describe_drawingarea_proxy(unittest.TestCase):
    
    def test_canvas_zoom_in_called(self):
        self.proxy.zoom_in()
        self.canvas.zoom_in.assert_called_once_with()
    
    def test_canvas_zoom_out_called(self):
        self.proxy.zoom_out()
        self.canvas.zoom_out.assert_called_once_with()
    
    def test_canvas_VertZoomIn_called(self):
        self.proxy.vertical_zoom_in()
        self.canvas.vertical_zoom_in.assert_called_once_with()
    
    def test_canvas_VertZoomOut_called(self):
        self.proxy.vertical_zoom_out()
        self.canvas.vertical_zoom_out.assert_called_once_with()
    
    def setUp(self):
        self.canvas = Mock(TimelineCanvas)
        self.proxy = DrawingAreaProxy(self.create_mainframe_object())
        
    def create_mainframe_object(self):
        mf = Mock(MainFrame)
        mf.main_panel = Mock(MainPanel)
        mf.main_panel.timeline_panel = Mock(TimelinePanel)
        mf.main_panel.timeline_panel.timeline_canvas = self.canvas
        mf.config = Mock()
        return mf
