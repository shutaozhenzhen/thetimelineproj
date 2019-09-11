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

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.container import Container
from timelinelib.canvas.data.event import Event
from timelinelib.canvas.data.subevent import Subevent
from timelinelib.db.strategies import DefaultContainerStrategy
from timelinelib.db.strategies import ExtendedContainerStrategy
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian


class ContainerStrategiesTestCase(UnitTestCase):

    def setUp(self):
        container = Container().update(
            human_time_to_gregorian("1 Jul 2014"),
            human_time_to_gregorian("1 Jul 2014"),
            "",
        )
        self.default_strategy = DefaultContainerStrategy(container)
        self.extended_strategy = ExtendedContainerStrategy(container)

    def _a_subevent_can_be_registred(self, strategy):
        subevent = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "1 Jan 2015"))
        strategy.register_subevent(subevent)
        self.assertEqual(1, len(strategy.container.subevents))
        self.assertTrue(subevent in strategy.container.subevents)
        self.assertEqual(subevent.get_time_period(), strategy.container.get_time_period())

    def _two_nonoverlapping_subevents_can_be_registred(self, strategy):
        subevent1 = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "10 Jan 2014"))
        subevent2 = self.a_subevent(time_period=gregorian_period("20 Jan 2014", "30 Jan 2014"))
        strategy.register_subevent(subevent1)
        strategy.register_subevent(subevent2)
        self.assertEqual(2, len(strategy.container.subevents))
        self.assertTrue(subevent1 in strategy.container.subevents)
        self.assertTrue(subevent2 in strategy.container.subevents)
        self.assertEqual(gregorian_period("1 Jan 2014", "30 Jan 2014"), strategy.container.get_time_period())

    def _two_overlapping_subevents_can_be_registred(self, strategy):
        subevent1 = self.a_subevent(time_period=gregorian_period("10 Jan 2014", "12 Jan 2014"))
        subevent2 = self.a_subevent(time_period=gregorian_period("11 Jan 2014", "16 Jan 2014"))
        strategy.register_subevent(subevent1)
        strategy.register_subevent(subevent2)
        self.assertEqual(2, len(strategy.container.subevents))
        self.assertTrue(subevent1 in strategy.container.subevents)
        self.assertTrue(subevent2 in strategy.container.subevents)

    def _a_subevent_is_only_registered_once(self, strategy):
        subevent = self.a_subevent()
        strategy.register_subevent(subevent)
        strategy.register_subevent(subevent)
        self.assertEqual(1, len(strategy.container.subevents))
        self.assertEqual(subevent, strategy.container.subevents[0])

    def _an_event_cannot_be_registred(self, strategy):
        subevent = Mock(Event)
        self.assertRaises(TypeError, strategy.register_subevent, subevent)
        self.assertEqual(0, len(strategy.container.subevents))

    def _none_cannot_be_registred(self, strategy):
        self.assertRaises(TypeError, strategy.register_subevent, None)
        self.assertEqual(0, len(strategy.container.subevents))

    def _a_subevent_can_be_unregistred(self, strategy):
        subevent = self.a_subevent()
        strategy.register_subevent(subevent)
        strategy.unregister_subevent(subevent)
        self.assertEqual(0, len(strategy.container.subevents))

    def _a_second_subevent_can_be_unregistred(self, strategy):
        subevent1 = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "10 Jan 2014"))
        subevent2 = self.a_subevent(time_period=gregorian_period("20 Jan 2014", "30 Jan 2014"))
        strategy.register_subevent(subevent1)
        strategy.register_subevent(subevent2)
        strategy.unregister_subevent(subevent2)
        self.assertEqual(1, len(strategy.container.subevents))
        self.assertTrue(subevent1 in strategy.container.subevents)
        self.assertEqual(gregorian_period("1 Jan 2014", "10 Jan 2014"), strategy.container.get_time_period())

    def _an_object_not_registered_is_ignored_when_unregistred(self, strategy):
        subevent = self.a_subevent()
        strategy.unregister_subevent(subevent)
        self.assertEqual(0, len(strategy.container.subevents))

    def _the_timeperiod_is_updated_when_the_subevent_time_period_changes(self, strategy):
        subevent = self.a_subevent(time_period=gregorian_period("1 Jan 2014", "10 Jan 2014"))
        strategy.register_subevent(subevent)
        self.assertEqual(subevent.get_time_period(), strategy.container.get_time_period())
        subevent.update_period_o(gregorian_period("1 Jan 2015", "10 Jan 2015"))
        strategy.update(subevent)
        self.assertEqual(subevent.get_time_period(), strategy.container.get_time_period())

    def a_subevent(self, time_period=gregorian_period("1 Jan 2014", "10 Jan 2014")):
        return Subevent().update(
            time_period.start_time,
            time_period.end_time,
            ""
        )


class describe_default_container_strategy(ContainerStrategiesTestCase):

    def test_disallsows_ends_today_subevents(self):
        self.assertFalse(self.default_strategy.allow_ends_today_on_subevents())

    def test_a_subevent_can_be_registredy(self):
        self._a_subevent_can_be_registred(self.default_strategy)

    def test_two_nonoverlapping_subevents_can_be_registred(self):
        self._two_nonoverlapping_subevents_can_be_registred(self.default_strategy)

    def test_two_overlapping_subevents_can_be_registred(self):
        self._two_overlapping_subevents_can_be_registred(self.default_strategy)
        self.assertEqual(gregorian_period("9 Jan 2014", "16 Jan 2014"),
                         self.default_strategy.container.get_time_period())

    def test_an_event_cannot_be_registred(self):
        self._an_event_cannot_be_registred(self.default_strategy)

    def test_none_cannot_be_registred(self):
        self._none_cannot_be_registred(self.default_strategy)

    def test_a_subevent_is_only_registered_once(self):
        self._a_subevent_is_only_registered_once(self.default_strategy)

    def test_a_subevent_can_be_unregistred(self):
        self._a_subevent_can_be_unregistred(self.default_strategy)

    def test_a_second_subevent_cn_be_unregistred(self):
        self._a_second_subevent_can_be_unregistred(self.default_strategy)

    def test_an_object_not_registered_is_ignored_when_unregistred(self):
        self._an_object_not_registered_is_ignored_when_unregistred(self.default_strategy)

    def test_the_timeperiod_is_updated_when_the_subevent_time_period_changes(self):
        self._the_timeperiod_is_updated_when_the_subevent_time_period_changes(self.default_strategy)


class describe_extended_container_strategy(ContainerStrategiesTestCase):

    def test_allsows_ends_today_subevents(self):
        self.assertTrue(self.extended_strategy.allow_ends_today_on_subevents())

    def test_a_subevent_can_be_registred(self):
        self._a_subevent_can_be_registred(self.extended_strategy)

    def test_two_nonoverlapping_subevents_can_be_registred(self):
        self._two_nonoverlapping_subevents_can_be_registred(self.extended_strategy)

    def test_two_overlapping_subevents_can_be_registred(self):
        self._two_overlapping_subevents_can_be_registred(self.extended_strategy)
        self.assertEqual(gregorian_period("10 Jan 2014", "16 Jan 2014"),
                         self.extended_strategy.container.get_time_period())

    def test_an_event_cannot_be_registred(self):
        self._an_event_cannot_be_registred(self.extended_strategy)

    def test_none_cannot_be_registred(self):
        self._none_cannot_be_registred(self.extended_strategy)

    def test_a_subevent_is_only_registered_once(self):
        self._a_subevent_is_only_registered_once(self.extended_strategy)

    def test_a_subevent_can_be_unregistred(self):
        self._a_subevent_can_be_unregistred(self.extended_strategy)

    def test_a_second_subevent_can_be_unregistred(self):
        self._a_second_subevent_can_be_unregistred(self.extended_strategy)

    def test_an_object_not_registered_is_ignored_when_unregistred(self):
        self._an_object_not_registered_is_ignored_when_unregistred(self.extended_strategy)

    def test_the_timeperiod_is_updated_when_the_subevent_time_period_changes(self):
        self._the_timeperiod_is_updated_when_the_subevent_time_period_changes(self.extended_strategy)


class describe_default_container_startegy_(UnitTestCase):
    """
    These tests should be merged into the class describe_default_container_startegy
    """

    def test_construction(self):
        self.given_strategy_with_container()
        self.assertEqual(self.container, self.strategy.container)

    def test_first_registered_event_decides_container_period(self):
        self.given_strategy_with_container()
        self.given_subevent1()
        self.strategy.register_subevent(self.subevent1)
        self.assert_equal_start(self.container, self.subevent1)
        self.assert_equal_end(self.container, self.subevent1)

    def test_second_registered_event_expands_container_period(self):
        # Container event:   +-------+
        # New sub-event:                 +-------+
        self.given_container_with_two_events_with_nonoverlapping_periods()
        self.assert_equal_start(self.container, self.subevent1)
        self.assert_equal_end(self.container, self.subevent2)

    def test_removing_one_event_contracts_container_period(self):
        # Container event:   +-------+
        # New sub-event:                 +-------+
        self.given_container_with_two_events_with_nonoverlapping_periods()
        self.strategy.unregister_subevent(self.subevent1)
        self.assert_equal_start(self.container, self.subevent2)
        self.assert_equal_end(self.container, self.subevent2)

    def test_updating_subevent_expands_container_period(self):
        # Container event:   +-------+
        # New sub-event:                 +-------+
        self.given_container_with_two_events_with_nonoverlapping_periods()
        self.subevent2.set_end_time(self.time("2000-05-01 10:01:01"))
        self.strategy.update(self.subevent2)
        self.assert_equal_start(self.container, self.subevent1)
        self.assert_equal_end(self.container, self.subevent2)

    def test_adding_partial_overlapping_event_moves_overlapped_event_backwards(self):
        # Container event:   +-------+
        # New sub-event:          +-------+
        self.given_container_with_two_events_with_overlapping_periods()
        self.assert_start_equals_end(self.subevent2, self.subevent1)

    def test_adding_partial_overlapping_event_moves_overlapped_event_forward(self):
        # Container event:        +-------+
        # New sub-event:     +-------+
        self.given_container_with_two_events_with_overlapping_periods_reversed_order()
        self.assert_start_equals_end(self.subevent2, self.subevent1)

    def test_adding_event_with_same_period_moves_overlapped_event_forward(self):
        # Container event:   +-------+
        # New sub-event:     +-------+
        self.given_container_with_two_events_with_same_periods()
        self.assert_start_equals_end(self.subevent1, self.subevent2)

    def test_adding_event_with_same_start_moves_overlapped_event_forward(self):
        # Container event:   +-------+
        # New sub-event:     +---+
        self.given_container_with_two_events_with_same_start_time()
        self.assert_start_equals_end(self.subevent1, self.subevent2)

    def test_overlapping_nonperiod_event_at_begining_moves_nonperiod_event_backwards(self):
        # Container event:    +
        # New sub-event:     +----------+
        self.given_strategy_with_container()
        self.given_event_overlapping_point_event()
        self.assert_start_equals_start(self.subevent1, self.subevent2)

    def test_overlapping_nonperiod_event_at_end_moves_nonperiod_event_forward(self):
        # Container event:             +
        # New sub-event:     +----------+
        self.given_strategy_with_container()
        self.given_event_overlapping_point_event2()
        self.assert_start_equals_end(self.subevent1, self.subevent2)

    def given_container_with_two_events_with_nonoverlapping_periods(self):
        self.given_strategy_with_container()
        self.given_two_events_with_nonoverlapping_periods()
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_container_with_two_events_with_overlapping_periods(self):
        self.given_strategy_with_container()
        self.given_two_overlapping_events()
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_container_with_two_events_with_overlapping_periods_reversed_order(self):
        self.given_strategy_with_container()
        self.given_two_overlapping_events()
        self.strategy.register_subevent(self.subevent2)
        self.strategy.register_subevent(self.subevent1)

    def given_container_with_two_events_with_same_periods(self):
        self.given_strategy_with_container()
        self.given_two_events_with_same_period()
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_container_with_two_events_with_same_start_time(self):
        self.given_strategy_with_container()
        self.given_two_events_with_same_start_time()
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_strategy_with_container(self):
        self.container = Container().update(
            self.time("2000-01-01 10:01:01"),
            self.time("2000-01-01 10:01:01"),
            "Container1"
        )
        self.container.set_id(self.new_id())
        self.strategy = DefaultContainerStrategy(self.container)

    def given_event_overlapping_point_event(self):
        self.subevent1 = Subevent().update(
            self.time("2000-05-01 10:02:01"),
            self.time("2000-05-01 10:02:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-05-01 10:01:01"),
            self.time("2000-07-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_event_overlapping_point_event2(self):
        self.subevent1 = Subevent().update(
            self.time("2000-07-01 10:00:01"),
            self.time("2000-07-01 10:00:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-05-01 10:01:01"),
            self.time("2000-07-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())
        self.strategy.register_subevent(self.subevent1)
        self.strategy.register_subevent(self.subevent2)

    def given_two_overlapping_events(self):
        self.subevent1 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-06-01 10:01:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-05-01 10:01:01"),
            self.time("2000-07-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())

    def given_two_events_with_same_period(self):
        self.subevent1 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-06-01 10:01:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-06-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())

    def given_two_events_with_same_start_time(self):
        self.subevent1 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-06-01 10:01:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-04-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())

    def given_two_events_with_nonoverlapping_periods(self):
        self.subevent1 = Subevent().update(
            self.time("2000-01-01 10:01:01"),
            self.time("2000-02-01 10:01:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())
        self.subevent2 = Subevent().update(
            self.time("2000-03-01 10:01:01"),
            self.time("2000-04-01 10:01:01"),
            "Container1"
        )
        self.subevent2.set_id(self.new_id())

    def given_subevent1(self):
        self.subevent1 = Subevent().update(
            self.time("2000-01-01 10:01:01"),
            self.time("2000-02-01 10:01:01"),
            "Container1"
        )
        self.subevent1.set_id(self.new_id())

    def assert_equal_start(self, obj1, obj2):
        self.assertEqual(obj1.get_time_period().start_time,
                         obj2.get_time_period().start_time)

    def assert_equal_end(self, obj1, obj2):
        self.assertEqual(obj1.get_time_period().end_time,
                         obj2.get_time_period().end_time)

    def assert_start_equals_end(self, obj1, obj2):
        self.assertEqual(obj1.get_time_period().start_time,
                         obj2.get_time_period().end_time)

    def assert_start_equals_start(self, obj1, obj2):
        self.assertEqual(obj1.get_time_period().start_time,
                         obj2.get_time_period().start_time)

    def time(self, tm):
        return self.time_type.parse_time(tm)

    def setUp(self):
        self.time_type = GregorianTimeType()
        self.id_counter = 0

    def new_id(self):
        self.id_counter += 1
        return self.id_counter
