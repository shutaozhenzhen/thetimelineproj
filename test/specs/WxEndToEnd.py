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


import sys

from timelinelib.test.cases.wxendtoend import WxEndToEndTestCase


class WxEndToEndSpec(WxEndToEndTestCase):

    def test_sidebar_gets_same_width_as_in_config(self):
        if WxEndToEndTestCase.HALT_GUI:
            self.config.set_show_sidebar(True)
            self.config.set_sidebar_width(300)
            self.start_timeline_and([
                self.check_that_sidebar_width_equals(300),
            ])

    def check_that_sidebar_width_equals(self, expected_width):
        def check():
            self.assertEqual(
                expected_width,
                self.find_component("main_frame -> splitter").GetSashPosition())
        return check
