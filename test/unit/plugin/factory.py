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
from timelinelib.plugin import factory
from timelinelib.test.cases.unit import UnitTestCase


class describe_plugin_factory(UnitTestCase):

    def test_can_return_a_named_plugin(self):
        plugin = factory.get_plugin(EVENTBOX_DRAWER, "Default Event box drawer")
        self.assertEquals(_("Default Event box drawer"), plugin.display_name())

    def test_can_return_another_named_plugin(self):
        plugin = factory.get_plugin(EVENTBOX_DRAWER, "Gradient Event box drawer")
        self.assertEquals(_("Gradient Event box drawer"), plugin.display_name())

    def test_returns_none_when_named_plugin_cant_be_found(self):
        plugin = factory.get_plugin(EVENTBOX_DRAWER, "xyz drawer")
        self.assertEquals(None, plugin)
