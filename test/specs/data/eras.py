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


from timelinelib.data.eras import InvalidOperationError
from timelinelib.data import Eras
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_gregorian_era
from timelinelib.test.utils import a_gregorian_era_with
from timelinelib.test.utils import a_numeric_era_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import numeric_period


class ErasTestCase(UnitTestCase):

    def test_default_has_an_empty_list(self):
        self.assertEqual([], self.eras.get_all())

    def setUp(self):
        self.eras = Eras()


class describe_cloning(ErasTestCase):

    def test_eras_are_cloned(self):
        self.eras.save_era(a_gregorian_era())
        self.eras.save_era(a_gregorian_era())
        clone = self.eras.clone()
        self.assertListIsCloneOf(clone.get_all(), self.eras.get_all())


class describe_saving_eras(ErasTestCase):

    def test_can_save(self):
        era = a_gregorian_era()
        self.eras.save_era(era)
        self.assertEqual(self.eras.get_all(), [era])

    def test_can_update(self):
        era = a_gregorian_era()
        self.eras.save_era(era)
        era.set_name("I'm the first era")
        self.eras.save_era(era)
        self.assertEqual(self.eras.get_all(), [era])

    def test_fails_if_existing_era_does_not_seem_to_be_found(self):
        era = a_gregorian_era()
        era.set_id(15)
        self.assertRaises(InvalidOperationError, self.eras.save_era, era)


class describe_overlapping_eras(ErasTestCase):

    def test_eras_are_returned_sorted(self):
        era1 = a_gregorian_era_with(start="1 Dec 2015", end="1 Jan 2016", color=(128, 255, 255))
        era2 = a_gregorian_era_with(start="30 Dec 2015", end="1 Feb 2016", color=(255, 0, 255))
        self.eras.save_era(era2)
        self.eras.save_era(era1)
        self.assertEqual(era1, self.eras.get_all()[0])


class describe_numeric_era_sublisting(ErasTestCase):

    def test_can_return_eras_visible_in_a_period(self):
        era1 = a_numeric_era_with(start=1, end=2)
        era2 = a_numeric_era_with(start=4, end=6)
        era3 = a_numeric_era_with(start=8, end=10)
        self.eras.save_era(era1)
        self.eras.save_era(era2)
        self.eras.save_era(era3)
        visible_eras = self.eras.get_in_period(numeric_period(3, 9))
        self.assertEquals([era2, era3], visible_eras)


class describe_gregorian_era_sublisting(ErasTestCase):

    def test_can_return_eras_visible_in_a_period(self):
        era1 = a_gregorian_era_with(start="1 Jan 2014", end="10 Jan 2014")
        era2 = a_gregorian_era_with(start="12 Jan 2014", end="16 Jan 2014")
        era3 = a_gregorian_era_with(start="18 Jan 2014", end="30 Jan 2014")
        self.eras.save_era(era1)
        self.eras.save_era(era2)
        self.eras.save_era(era3)
        visible_eras = self.eras.get_in_period(gregorian_period("16 Jan 2014", "20 Jan 2014"))
        self.assertEquals([era2, era3], visible_eras)
