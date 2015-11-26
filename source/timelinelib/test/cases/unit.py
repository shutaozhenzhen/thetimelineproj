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


import random
import unittest

from timelinelib.time.gregoriantime import GregorianTimeType


class UnitTestCase(unittest.TestCase):

    HALT_GUI = False

    def assertPeriodsEqual(self, first, second, time_type=GregorianTimeType()):
        message = "Periods not equal.\n  First:  %s \"%s\"\n  Second: %s \"%s\"" % (
            first,
            time_type.format_period(first),
            second,
            time_type.format_period(second),
        )
        self.assertEqual(first, second, message)

    def assertListIsCloneOf(self, cloned_list, original_list):
        self.assertEqual(cloned_list, original_list)
        self.assertTrue(cloned_list is not original_list)
        for i in range(len(cloned_list)):
            self.assertIsCloneOf(cloned_list[i], original_list[i])

    def assertIsCloneOf(self, clone, original):
        self.assertEqual(clone, original)
        self.assertTrue(clone is not original, "%r" % clone)

    def assertInstanceNotIn(self, object_, list_):
        for element in list_:
            if element is object_:
                self.fail("%r was in list" % object_)

    def assertEqNeImplementationIsCorrect(self, create_fn, modifiers):
        (modification_description, modifier_fn) = get_random_modifier(modifiers)
        one = modifier_fn(create_fn())
        other = modifier_fn(create_fn())
        fail_message_one_other = "%r vs %r (%s)" % (one, other,
                                                    modification_description)
        self.assertTrue(type(one) == type(other), fail_message_one_other)
        self.assertFalse(one is None, fail_message_one_other)
        self.assertTrue(one is not None, fail_message_one_other)
        self.assertTrue(one is not other, fail_message_one_other)
        self.assertFalse(one is other, fail_message_one_other)
        self.assertTrue(one == other, fail_message_one_other)
        self.assertFalse(one != other, fail_message_one_other)
        self.assertTrue(one == one, fail_message_one_other)
        self.assertFalse(one != one, fail_message_one_other)
        (modification_description, modifier_fn) = get_random_modifier(modifiers)
        modified = modifier_fn(other)
        fail_message_modified_one = "%r vs %r (%s)" % (modified, one,
                                                       modification_description)
        self.assertTrue(type(modified) == type(one), fail_message_modified_one)
        self.assertTrue(modified is not one, fail_message_modified_one)
        self.assertFalse(modified is one, fail_message_modified_one)
        self.assertTrue(modified != one, fail_message_modified_one)
        self.assertFalse(modified == one, fail_message_modified_one)


def get_random_modifier(modifiers):
    return random.choice(modifiers)
