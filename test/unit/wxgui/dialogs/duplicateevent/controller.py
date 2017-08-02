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


from mock import Mock

from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data import TimePeriod
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import gregorian_period
from timelinelib.wxgui.dialogs.duplicateevent.controller import BACKWARD
from timelinelib.wxgui.dialogs.duplicateevent.controller import BOTH
from timelinelib.wxgui.dialogs.duplicateevent.controller import DuplicateEventDialogController
from timelinelib.wxgui.dialogs.duplicateevent.controller import EventDuplicator
from timelinelib.wxgui.dialogs.duplicateevent.controller import FORWARD
from timelinelib.wxgui.dialogs.duplicateevent.view import DuplicateEventDialog


class DuplicateEventDialogTestCase(UnitTestCase):

    def setUp(self):
        self.view = Mock(DuplicateEventDialog)
        self.view.GetMovePeriodFn.return_value = self._create_move_period_fn_mock()
        self.event = an_event_with(time="1 Jan 2010", text="foo")
        self.event_duplicator = Mock(EventDuplicator)
        self.controller = DuplicateEventDialogController(self.view)
        self.controller.on_init(self.event, event_duplicator=self.event_duplicator)

    def _create_move_period_fn_mock(self):
        self.move_period_fn = Mock()
        self.move_period_fn.return_value = gregorian_period(
            "1 Aug 2010",
            "1 Aug 2010"
        )
        return self.move_period_fn

    def duplicate_with(self, count, freq, direction):
        self.view.GetCount.return_value = count
        self.view.GetFrequency.return_value = freq
        self.view.GetDirection.return_value = direction
        self.controller.on_ok(None)

    def assertMovedPeriod(self, num_list):
        self.assertEqual(
            self.move_period_fn.call_args_list,
            [((self.event.get_time_period(), num), {}) for num in num_list]
        )


class describe_gui(DuplicateEventDialogTestCase):

    def test_it_can_be_created(self):
        self.show_dialog(DuplicateEventDialog, None, MemoryDB(), None)


class describe_default_values(DuplicateEventDialogTestCase):

    def test_number_of_duplicates_should_be_1(self):
        self.view.SetCount.assert_called_with(1)

    def test_first_period_should_be_selected(self):
        self.view.SelectMovePeriodFnAtIndex.assert_called_with(0)

    def test_frequency_should_be_one(self):
        self.view.SetFrequency.assert_called_with(1)

    def test_direction_should_be_forward(self):
        self.view.SetDirection.assert_called_with(FORWARD)


class describe_duplicating(DuplicateEventDialogTestCase):

    def setUp(self):
        DuplicateEventDialogTestCase.setUp(self)
        self.duplicate_with(count=2, freq=1, direction=FORWARD)

    def test_one_transaction_is_made(self):
        self.assertEqual(1, self.event_duplicator.duplicate.call_count)

    def test_the_dialog_should_close(self):
        self.assertTrue(self.view.Close.assert_called)


class describe_duplicate_errors(DuplicateEventDialogTestCase):

    def test_invalid_direction_raises_exception(self):
        self.assertRaises(
            Exception,
            self.controller._calculate_indicies, None, None
        )

    def test_none_period_failure_is_handled(self):
        self.move_period_fn.return_value = None
        self.duplicate_with(count=1, freq=1, direction=FORWARD)
        self.view.HandleDateErrors.assert_called_with(1)
        self.assertTrue(self.view.Close.called)


class describe_duplicate_with_different_settings(DuplicateEventDialogTestCase):

    def test_count_1_freq_1_direction_forward(self):
        self.duplicate_with(count=1, freq=1, direction=FORWARD)
        self.assertMovedPeriod([1])

    def test_count_1_freq_1_direction_backward(self):
        self.duplicate_with(count=1, freq=1, direction=BACKWARD)
        self.assertMovedPeriod([-1])

    def test_count_1_freq_1_direction_both(self):
        self.duplicate_with(count=1, freq=1, direction=BOTH)
        self.assertMovedPeriod([-1, 1])

    def test_count_2_freq_1_direction_forward(self):
        self.duplicate_with(count=2, freq=1, direction=FORWARD)
        self.assertMovedPeriod([1, 2])

    def test_count_2_freq_1_direction_backward(self):
        self.duplicate_with(count=2, freq=1, direction=BACKWARD)
        self.assertMovedPeriod([-2, -1])

    def test_count_2_freq_1_direction_both(self):
        self.duplicate_with(count=2, freq=1, direction=BOTH)
        self.assertMovedPeriod([-2, -1, 1, 2])

    def test_count_1_freq_2_direction_forward(self):
        self.duplicate_with(count=1, freq=2, direction=FORWARD)
        self.assertMovedPeriod([2])

    def test_count_1_freq_2_direction_backward(self):
        self.duplicate_with(count=1, freq=2, direction=BACKWARD)
        self.assertMovedPeriod([-2])

    def test_count_1_freq_2_direction_both(self):
        self.duplicate_with(count=1, freq=2, direction=BOTH)
        self.assertMovedPeriod([-2, 2])


class describe_event_duplicator(UnitTestCase):

    def test_duplicate_event(self):
        event = self.db.new_event(
            time_period=gregorian_period("1 Jan 2014", "31 Jan 2014")
        ).save()
        self.duplicate(event, [
            gregorian_period("1 Jan 2015", "31 Jan 2015"),
            gregorian_period("1 Jan 2016", "31 Jan 2016"),
        ])
        self.assertEqual(
            [
                gregorian_period("1 Jan 2014", "31 Jan 2014"),
                gregorian_period("1 Jan 2015", "31 Jan 2015"),
                gregorian_period("1 Jan 2016", "31 Jan 2016"),
            ],
            [
                event.time_period
                for event
                in self.db.get_all_events()
            ]
        )

    def test_duplicate_subevent(self):
        container = self.db.new_container().save()
        subevent = self.db.new_subevent(
            time_period=gregorian_period("1 Jan 2015", "5 Jan 2015"),
            container=container
        ).save()
        self.duplicate(subevent, [
            gregorian_period("5 Jan 2015", "10 Jan 2015"),
            gregorian_period("10 Jan 2015", "15 Jan 2015"),
        ])
        self.assertEqual(
            [
                gregorian_period("1 Jan 2015", "5 Jan 2015"),
                gregorian_period("5 Jan 2015", "10 Jan 2015"),
                gregorian_period("10 Jan 2015", "15 Jan 2015"),
            ],
            [
                event.time_period
                for event
                in self.db.get_all_events()
                if event.is_subevent()
            ]
        )

    def test_duplicate_container(self, length=GregorianDelta.from_days(2),
                                       days_apart=GregorianDelta.from_days(2),
                                       move=GregorianDelta.from_days(3)):
        start = GregorianDateTime.from_ymd(2017, 1, 1).to_time()
        event_period = TimePeriod(start, start + length)
        container = self.db.new_container().save()
        self.db.new_subevent(
            time_period=event_period,
            container=container
        ).save()
        self.db.new_subevent(
            time_period=event_period.move_delta(event_period.delta()).move_delta(days_apart),
            container=container
        ).save()
        self.duplicate(container, [
            container.time_period.move_delta(1 * move),
            container.time_period.move_delta(2 * move),
        ])
        self.assertEqual(
            [
                container.time_period.move_delta(0 * move),
                container.time_period.move_delta(1 * move),
                container.time_period.move_delta(2 * move),
            ],
            [
                event.time_period
                for event
                in self.db.get_all_events()
                if event.is_container()
            ]
        )

    def duplicate(self, *args, **kwargs):
        index, is_in_transaction, history_before = self.db._transactions.status
        EventDuplicator().duplicate(*args, **kwargs)
        index, is_in_transaction, history_after = self.db._transactions.status
        self.assertEqual(len(history_after), len(history_before) + 1)

    def setUp(self):
        self.db = MemoryDB()
