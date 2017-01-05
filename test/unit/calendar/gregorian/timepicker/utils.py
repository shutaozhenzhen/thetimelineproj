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


from timelinelib.calendar.gregorian.timepicker.utils import DAY_INDEX
from timelinelib.calendar.gregorian.timepicker.utils import gregorian_date_to_parts
from timelinelib.calendar.gregorian.timepicker.utils import MONTH_INDEX
from timelinelib.calendar.gregorian.timepicker.utils import parts_to_gregorian_date
from timelinelib.calendar.gregorian.timepicker.utils import YEAR_INDEX
from timelinelib.test.cases.unit import UnitTestCase


FORMAT_YMD = (YEAR_INDEX, MONTH_INDEX, DAY_INDEX)
FORMAT_DMY = (DAY_INDEX, MONTH_INDEX, YEAR_INDEX)


class describe_gregorian_date_picker_parts_to_date_conversion(UnitTestCase):

    def test_it_converts_regular_date(self):
        self.assertEqual(
            parts_to_gregorian_date(FORMAT_YMD, ["2015", "12", "17"], False),
            (2015, 12, 17)
        )

    def test_it_converts_bc_date(self):
        self.assertEqual(
            parts_to_gregorian_date(FORMAT_YMD, ["1401", "12", "17"], True),
            (-1400, 12, 17)
        )

    def test_it_converts_other_format(self):
        self.assertEqual(
            parts_to_gregorian_date(FORMAT_DMY, ["12", "10", "1999"], False),
            (1999, 10, 12)
        )

    def test_it_ignores_zero(self):
        self.assertEqual(
            parts_to_gregorian_date(FORMAT_YMD, ["0001", "02", "03"], False),
            (1, 2, 3)
        )


class describe_gregorian_date_picker_date_to_parts_conversion(UnitTestCase):

    def test_it_converts_regular_date(self):
        self.assertEqual(
            gregorian_date_to_parts(FORMAT_YMD, (2015, 12, 17)),
            (["2015", "12", "17"], False)
        )

    def test_it_converts_bc_date(self):
        self.assertEqual(
            gregorian_date_to_parts(FORMAT_YMD, (-1400, 12, 17)),
            (["1401", "12", "17"], True)
        )

    def test_it_converts_other_format(self):
        self.assertEqual(
            gregorian_date_to_parts(FORMAT_DMY, (1999, 10, 12)),
            (["12", "10", "1999"], False)
        )

    def test_it_zero_pads(self):
        self.assertEqual(
            gregorian_date_to_parts(FORMAT_YMD, (1, 2, 3)),
            (["0001", "02", "03"], False)
        )
