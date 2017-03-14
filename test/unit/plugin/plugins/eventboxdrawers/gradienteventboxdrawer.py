# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


from timelinelib.plugin.factory import EVENTBOX_DRAWER
from timelinelib.plugin.plugins.eventboxdrawers.gradienteventboxdrawer import GradientEventBoxDrawer
from timelinelib.test.cases.unit import UnitTestCase


class describe_gradient_event_box_drawer(UnitTestCase):

    def test_is_a_plugin(self):
        self.assertTrue(self.plugin.isplugin())

    def test_is_an_event_box_drawer(self):
        self.assertEquals(EVENTBOX_DRAWER, self.plugin.service())

    def test_has_a_display_name(self):
        self.assertTrue(len(self.plugin.display_name()) > 0)

    def test_overrides_draw_background(self):
        self.assertTrue(callable(getattr(self.plugin.run(), "_draw_background")))

    def setUp(self):
        self.plugin = GradientEventBoxDrawer()
