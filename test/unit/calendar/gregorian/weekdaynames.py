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


from timelinelib.test.cases.unit import UnitTestCase
import timelinelib.calendar.gregorian.weekdaynames


class describe_weekday_names(UnitTestCase):

    def test_abbreviated_weekday_name_for_0_should_be_mon_translated(self):
        self.assertEqual(
            _("Mon"),
            timelinelib.calendar.gregorian.weekdaynames.abbreviated_name_of_weekday(0))

    def test_abbreviated_weekday_name_for_6_should_be_sun_translated(self):
        self.assertEqual(
            _("Sun"),
            timelinelib.calendar.gregorian.weekdaynames.abbreviated_name_of_weekday(6))
