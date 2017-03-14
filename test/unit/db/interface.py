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


from timelinelib.db.interface import ContainerStrategy
from timelinelib.test.cases.unit import UnitTestCase


class describe_container_strategy_interface(UnitTestCase):

    def test_construction(self):
        self.given_strategy_with_none_container()
        self.assertEqual(None, self.strategy.container)

    def test_register_subevent_NotImplemented(self):
        self.given_strategy_with_none_container()
        self.assertRaises(NotImplementedError, self.strategy.register_subevent, None)

    def test_unregister_subevent_NotImplemented(self):
        self.given_strategy_with_none_container()
        self.assertRaises(NotImplementedError, self.strategy.unregister_subevent, None)

    def test_update_subevent_NotImplemented(self):
        self.given_strategy_with_none_container()
        self.assertRaises(NotImplementedError, self.strategy.update, None)

    def test_allow_ends_today_NotImplemented(self):
        self.given_strategy_with_none_container()
        self.assertRaises(NotImplementedError, self.strategy.allow_ends_today_on_subevents)

    def given_strategy_with_none_container(self):
        self.strategy = ContainerStrategy(None)

    def setUp(self):
        UnitTestCase.setUp(self)
