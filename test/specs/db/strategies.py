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


from mock import Mock

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.db.strategies import DefaultContainerStrategy
from timelinelib.db.strategies import ExtendedContainerStrategy
from timelinelib.data.event import Event
from timelinelib.data.subevent import Subevent
from timelinelib.data.container import Container
from timelinelib.test.utils import gregorian_period
from timelinelib.data.timeperiod import TimePeriod
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.test.utils import human_time_to_gregorian


class ContainerStrategiesTestCase(UnitTestCase):
    """
    To be tested:
        Rgeistering a None object
        Time periods when registering 2 subevents with overlapping time period.
           The result depends on strategy.
        The Update method
    """

    def setUp(self):
        container = Mock(Container)
        container.events = []
        container.get_time_period.return_value = TimePeriod(GregorianTimeType(),
                                                            human_time_to_gregorian("1 Jul 2014"),
                                                            human_time_to_gregorian("1 Jul 2014"))
        self.default_strategy = DefaultContainerStrategy(container)
        self.extended_strategy = ExtendedContainerStrategy(container)

    def tearDown(self):
        pass

    def _a_subevent_can_be_registred(self, strategy):
        subevent = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "1 Jan 2015"))
        strategy.register_subevent(subevent)
        self.assertEqual(1, len(strategy.container.events))
        self.assertEqual(subevent, strategy.container.events[0])
        subevent.register_container.assert_called_with(strategy.container)
        self.assertEqual(subevent.get_time_period(), strategy.container.get_time_period())

    def _two_nonoverlapping_subevents_can_be_registred(self, strategy):
        subevent1 = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "10 Jan 2014"))
        subevent2 = self.a_subevent(time_period=gregorian_period("20 Jan 2014", "30 Jan 2014"))
        strategy.register_subevent(subevent1)
        strategy.register_subevent(subevent2)
        self.assertEqual(2, len(strategy.container.events))
        self.assertTrue(subevent1 in strategy.container.events)
        self.assertTrue(subevent2 in strategy.container.events)
        subevent1.register_container.assert_called_with(strategy.container)
        subevent2.register_container.assert_called_with(strategy.container)
        self.assertEqual(gregorian_period("1 Jan 2014", "30 Jan 2014"), strategy.container.get_time_period())

    def _a_subevent_is_only_registered_once(self, strategy):
        subevent = self.a_subevent()
        strategy.register_subevent(subevent)
        strategy.register_subevent(subevent)
        self.assertEqual(1, len(strategy.container.events))
        self.assertEqual(subevent, strategy.container.events[0])
        subevent.register_container.assert_called_with(strategy.container)

    def _an_event_cannot_be_registred(self, strategy):
        subevent = Mock(Event)
        self.assertRaises(TypeError, strategy.register_subevent, subevent)
        self.assertEqual(0, len(strategy.container.events))

    def _a_subevent_can_be_unregistred(self, strategy):
        subevent = self.a_subevent()
        strategy.register_subevent(subevent)
        strategy.unregister_subevent(subevent)
        self.assertEqual(0, len(strategy.container.events))
        self.assertEqual(subevent.get_time_period(), strategy.container.get_time_period())

    def _a_second_subevent_cn_be_unregistred(self, strategy):
        subevent1 = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "10 Jan 2014"))
        subevent2 = self.a_subevent(time_period=gregorian_period("20 Jan 2014", "30 Jan 2014"))
        strategy.register_subevent(subevent1)
        strategy.register_subevent(subevent2)
        strategy.unregister_subevent(subevent2)
        self.assertEqual(1, len(strategy.container.events))
        self.assertTrue(subevent1 in strategy.container.events)
        self.assertEqual(gregorian_period("1 Jan 2014", "10 Jan 2014"), strategy.container.get_time_period())

    def _an_object_not_registered_is_ignored_when_unregistred(self, strategy):
        subevent = self.a_subevent()
        strategy.unregister_subevent(subevent)
        self.assertEqual(0, len(strategy.container.events))

    def a_subevent(self, time_period=gregorian_period("1 Jan 2014", "10 Jan 2014")):
        subevent = Mock(Subevent)
        subevent.get_time_period.return_value = time_period
        return subevent


class describe_default_container_strategy(ContainerStrategiesTestCase):

    def test_disallsows_ends_today_subevents(self):
        self.assertFalse(self.default_strategy.allow_ends_today_on_subevents())

    def test_a_subevent_can_be_registredy(self):
        self._a_subevent_can_be_registred(self.default_strategy)

    def test_two_nonoverlapping_subevents_can_be_registred(self):
        self._two_nonoverlapping_subevents_can_be_registred(self.default_strategy)

    def test_an_event_cannot_be_registred(self):
        self._an_event_cannot_be_registred(self.default_strategy)

    def test_a_subevent_is_only_registered_once(self):
        self._a_subevent_is_only_registered_once(self.default_strategy)

    def test_a_subevent_can_be_unregistred(self):
        self._a_subevent_can_be_unregistred(self.default_strategy)

    def test_a_second_subevent_cn_be_unregistred(self):
        self._a_second_subevent_cn_be_unregistred(self.default_strategy)

    def test_an_object_not_registered_is_ignored_when_unregistred(self):
        self._an_object_not_registered_is_ignored_when_unregistred(self.default_strategy)


class describe_extended_container_strategy(ContainerStrategiesTestCase):

    def test_allsows_ends_today_subevents(self):
        self.assertTrue(self.extended_strategy.allow_ends_today_on_subevents())

    def test_a_subevent_can_be_registred(self):
        self._a_subevent_can_be_registred(self.extended_strategy)

    def test_two_nonoverlapping_subevents_can_be_registred(self):
        self._two_nonoverlapping_subevents_can_be_registred(self.default_strategy)

    def test_an_event_cannot_be_registred(self):
        self._an_event_cannot_be_registred(self.default_strategy)

    def test_a_subevent_is_only_registered_once(self):
        self._a_subevent_is_only_registered_once(self.extended_strategy)

    def test_a_subevent_can_be_unregistred(self):
        self._a_subevent_can_be_unregistred(self.extended_strategy)

    def test_a_second_subevent_cn_be_unregistred(self):
        self._a_second_subevent_cn_be_unregistred(self.extended_strategy)

    def test_an_object_not_registered_is_ignored_when_unregistred(self):
        self._an_object_not_registered_is_ignored_when_unregistred(self.extended_strategy)
