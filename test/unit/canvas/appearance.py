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
from unittest.mock import sentinel
import wx

from timelinelib.canvas.appearance import Appearance
from timelinelib.test.cases.unit import UnitTestCase


class describe_appearance(UnitTestCase):

    def test_has_default_value(self):
        self.assertEqual(self.appearance.get_legend_visible(), True)

    def test_can_change_value(self):
        self.assertEqual(self.appearance.get_legend_visible(), True)
        self.appearance.set_legend_visible(False)
        self.assertEqual(self.appearance.get_legend_visible(), False)

    def test_change_of_value_triggers(self):
        listener = Mock()
        self.appearance.listen_for_any(listener)
        self.appearance.set_legend_visible(False)
        self.appearance.set_legend_visible(False)
        self.appearance.set_never_use_time(True)
        self.assertEqual(listener.call_count, 2)

    def test_has_properties(self):
        self.appearance.get_never_use_time()
        self.appearance.set_never_use_time(sentinel.VALUE)

    def setUp(self):
        self.app = wx.App()
        self.appearance = Appearance()
