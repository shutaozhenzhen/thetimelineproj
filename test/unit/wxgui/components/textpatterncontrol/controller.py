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


from mock import Mock

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.components.textpatterncontrol.view import TextPatternControl
from timelinelib.wxgui.components.textpatterncontrol.controller import TextPatternControlController


class describe_text_pattern_control(UnitTestCase):

    def test_it_sets_value_depending_on_separators_and_parts(self):
        self.controller.set_separators(["a", "b"])
        self.controller.set_parts(["1", "2", "3"])
        self.view.SetValue.assert_called_with("1a2b3")

    def test_it_gets_parts_depending_on_separators_and_value(self):
        self.controller.set_separators(["a", "b"])
        self.view.GetValue.return_value = "1a2b3"
        self.assertEqual(self.controller.get_parts(), ["1", "2", "3"])

    def setUp(self):
        UnitTestCase.setUp(self)
        self.view = Mock(TextPatternControl)
        self.view.GetValue.return_value = ""
        self.view.GetSelection.return_value = (0, 0)
        self.controller = TextPatternControlController(self.view)
        self.controller.on_init()
