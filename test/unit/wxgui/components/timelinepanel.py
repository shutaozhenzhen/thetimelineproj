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


from unittest.mock import Mock
import wx

from timelinelib.wxgui.components.timelinepanel import TimelinePanel
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.test.cases.unit import UnitTestCase


class describe_timelinepanel(UnitTestCase):

    def test_can_be_created(self):
        self.assertTrue(self.panel is not None)

    def setUp(self):
        self.app = self.get_wxapp()
        self.parent = wx.Dialog(None)
        self.config = Mock()
        self.config.show_toolbar = False
        self.status_bar_adapter = Mock()
        self.main_frame = Mock(MainFrame)
        self.panel = TimelinePanel(self.parent, self.config, self.status_bar_adapter, self.main_frame)

    def tearDown(self):
        self.app.Destroy()
