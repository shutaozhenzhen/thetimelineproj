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


import re

from unittest.mock import Mock

from timelinelib.canvas.data.transactions import TransactionError
from timelinelib.canvas.data.transactions import Transactions
from timelinelib.test.cases.unit import UnitTestCase


class describe_transactions(UnitTestCase):

    def test_has_initial_value(self):
        self.assertHasValue(ImmutableText(""))

    def test_value_changes_after_new_transaction(self):
        with self.transactions.new("Add one") as t:
            t.append("1")
        self.assertHasValue(ImmutableText("1"))

    def test_nested_transactions_only_stores_first(self):
        with self.transactions.new("Outer") as t:
            t.append("1")
            with self.transactions.new("Inner 1") as t1:
                t1.append("2")
            t.append(",")
            with self.transactions.new("Inner 2") as t2:
                t2.append("3")
            t.append("4")
        self.assertHasValue(ImmutableText("12,34"))

    def test_value_is_temporarily_changed_during_transaction(self):
        try:
            with self.transactions.new("Outer") as t1:
                t1.append("1")
                self.assertHasValue(ImmutableText("1"))
                with self.transactions.new("Inner") as t2:
                    t2.append("2")
                    self.assertHasValue(ImmutableText("12"))
                    raise TestError()
        except TestError:
            self.assertHasValue(ImmutableText(""))

    def test_inner_transaction_failure_only_affects_inner_transaction(self):
        with self.transactions.new("t1") as t1:
            t1.append("1")
            try:
                with self.transactions.new("t2") as t2:
                    t2.append("2")
                    raise TestError()
            except TestError:
                pass
        self.assertHasValue(ImmutableText("1"))

    def test_has_initial_history(self):
        self.assertEqual(self.transactions.status, (0, False, [
            (self.INITIAL, ImmutableText("")),
        ]))

    def test_history_is_added(self):
        with self.transactions.new("t1") as t:
            t.append("1")
        with self.transactions.new("t2") as t:
            t.append("2")
        self.assertEqual(self.transactions.status, (2, False, [
            (self.INITIAL, ImmutableText("")),
            ("t1", ImmutableText("1")),
            ("t2", ImmutableText("12")),
        ]))

    def test_history_can_be_cleared(self):
        with self.transactions.new("t1") as t:
            t.append("1")
        with self.transactions.new("t2") as t:
            t.append("2")
        self.transactions.clear()
        self.assertEqual(self.transactions.status, (0, False, [
            ("t2", ImmutableText("12")),
        ]))

    def test_can_move_around_in_history(self):
        with self.transactions.new("t1") as t:
            t.append("1")
        with self.transactions.new("t2") as t:
            t.append("2")
        self.assertEqual(self.transactions.status, (2, False, [
            (self.INITIAL, ImmutableText("")),
            ("t1", ImmutableText("1")),
            ("t2", ImmutableText("12")),
        ]))
        self.transactions.move(1)
        self.assertEqual(self.transactions.status, (1, False, [
            (self.INITIAL, ImmutableText("")),
            ("t1", ImmutableText("1")),
            ("t2", ImmutableText("12")),
        ]))

    def test_future_history_is_erased_when_new_transaction(self):
        with self.transactions.new("t1") as t:
            t.append("1")
        with self.transactions.new("t2") as t:
            t.append("2")
        self.transactions.move(1)
        self.assertEqual(self.transactions.status, (1, False, [
            (self.INITIAL, ImmutableText("")),
            ("t1", ImmutableText("1")),
            ("t2", ImmutableText("12")),
        ]))
        with self.transactions.new("t3") as t:
            t.append("3")
        self.assertEqual(self.transactions.status, (2, False, [
            (self.INITIAL, ImmutableText("")),
            ("t1", ImmutableText("1")),
            ("t3", ImmutableText("13")),
        ]))

    def test_history_is_pruned(self):
        for number in range(self.MAX+1):
            with self.transactions.new("t{0}".format(number)) as t:
                t.append("x")
        (current_index, in_transaction, states) = self.transactions.status
        self.assertEqual(len(states), self.MAX)
        self.assertEqual(current_index, self.MAX-1)

    def test_status_reports_if_in_transaction(self):
        with self.transactions.new("Test"):
            self.assertEqual(self.transactions.status, (0, True, [
                (self.INITIAL, ImmutableText("")),
            ]))

    def test_raises_exception_if_comitting_twice(self):
        t = self.transactions.new("Test")
        t.commit()
        with self.assertRaisesTransactionError("Test"):
            t.commit()

    def test_raises_exception_if_rollbacking_twice(self):
        t = self.transactions.new("Test")
        t.rollback()
        with self.assertRaisesTransactionError("Test"):
            t.rollback()

    def test_raises_exception_if_modifying_non_current_transaction(self):
        with self.transactions.new("t1") as t1:
            t1.append("1")
            with self.transactions.new("t2") as t2:
                with self.assertRaisesTransactionError("t1"):
                    t1.append("2")

    def test_raises_exception_if_moving_in_history_while_in_transaction(self):
        with self.transactions.new("t1"):
            pass
        with self.transactions.new("t2"):
            with self.assertRaisesTransactionError("t2"):
                self.transactions.move(0)

    def test_raises_exception_if_moving_in_history_out_of_range(self):
        with self.transactions.new("t1"):
            pass
        with self.assertRaises(ValueError):
            self.transactions.move(-1)
        self.transactions.move(0)
        self.transactions.move(1)
        with self.assertRaises(ValueError):
            self.transactions.move(2)

    def test_raises_exception_if_clearing_history_while_in_transaction(self):
        with self.transactions.new("t2"):
            with self.assertRaisesTransactionError("t2"):
                self.transactions.clear()

    def test_raises_exception_if_history_size_is_too_small(self):
        Transactions(None, history_size=1)
        with self.assertRaises(ValueError):
            Transactions(None, history_size=-4)

    def test_notifies_on_commit(self):
        fn = Mock()
        self.transactions.listen_for_any(fn)
        with self.transactions.new("t1") as t:
            t.append("1")
        with self.assertRaises(ValueError):
            with self.transactions.new("t2") as t:
                t.append("2")
                raise ValueError()
        self.assertEqual(fn.call_count, 1)

    def test_notifies_on_move(self):
        fn = Mock()
        self.transactions.listen_for_any(fn)
        self.transactions.move(0)
        self.assertEqual(fn.call_count, 1)

    def test_notifies_on_clear(self):
        fn = Mock()
        self.transactions.listen_for_any(fn)
        self.transactions.clear()
        self.assertEqual(fn.call_count, 1)

    def assertHasValue(self, value):
        self.assertEqual(self.transactions.value, value)

    def assertRaisesTransactionError(self, name):
        return self.assertRaisesRegex(
            TransactionError,
            re.escape("Transaction(name='{0}', ...)".format(name))
        )

    def setUp(self):
        self.MAX = 5
        self.INITIAL = "initial"
        self.transactions = Transactions(
            ImmutableText(""),
            initial_name=self.INITIAL,
            history_size=self.MAX
        )


class ImmutableText(str):

    def append(self, text):
        return ImmutableText(self + text)


class TestError(Exception):
    pass
