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


from timelinelib.canvas.data.subevent import Subevent
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import a_container_with
from timelinelib.test.utils import a_subevent
from timelinelib.test.utils import a_subevent_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.test.utils import SUBEVENT_MODIFIERS


class describe_subevent(UnitTestCase):

    def test_can_get_values(self):
        event = Subevent().update(
            start_time=human_time_to_gregorian("11 Jul 2014"),
            end_time=human_time_to_gregorian("12 Jul 2014"),
            text="a day in my life"
        )
        self.assertEqual(event.get_id(), None)
        self.assertEqual(event.get_time_period(),
                         gregorian_period("11 Jul 2014", "12 Jul 2014"))
        self.assertEqual(event.get_text(), "a day in my life")
        self.assertEqual(event.get_category(), None)
        self.assertEqual(event.get_fuzzy(), False)
        self.assertEqual(event.get_locked(), False)
        self.assertEqual(event.get_ends_today(), False)
        self.assertEqual(event.get_description(), None)
        self.assertEqual(event.get_icon(), None)
        self.assertEqual(event.get_hyperlink(), None)
        self.assertEqual(event.get_progress(), None)
        self.assertEqual(event.get_container(), None)

    def test_can_set_values(self):
        self.assertEqual(
            a_subevent().set_id(15).get_id(),
            15)
        self.assertEqual(
            a_subevent().set_time_period(gregorian_period("1 Jan 2014", "1 Jan 2015")).get_time_period(),
            gregorian_period("1 Jan 2014", "1 Jan 2015"))
        self.assertEqual(
            a_subevent().set_text("cool").get_text(),
            "cool")
        a_parent_category = a_category_with(name="work")
        self.assertEqual(
            a_subevent().set_category(a_parent_category).get_category(),
            a_parent_category)
        self.assertEqual(
            a_subevent().set_fuzzy(True).get_fuzzy(),
            True)
        self.assertEqual(
            a_subevent().set_locked(True).get_locked(),
            True)
        self.assertEqual(
            a_subevent().set_ends_today(True).get_ends_today(),
            True)
        self.assertEqual(
            a_subevent().set_description("cool").get_description(),
            "cool")
        an_icon = "really not an icon"
        self.assertEqual(
            a_subevent().set_icon(an_icon).get_icon(),
            an_icon)
        self.assertEqual(
            a_subevent().set_hyperlink("http://google.com").get_hyperlink(),
            "http://google.com")
        self.assertEqual(
            a_subevent().set_progress(88).get_progress(),
            88)
        self.assertEqual(
            a_subevent().set_alert("2015-01-07 00:00:00;hoho").get_alert(),
            "2015-01-07 00:00:00;hoho")

    def test_can_be_compared(self):
        self.assertEqNeImplementationIsCorrect(a_subevent, SUBEVENT_MODIFIERS)

    def test_is_not_a_milestone(self):
        self.assertFalse(a_subevent().is_milestone())

    def test_can_change_container(self):
        subevent = a_subevent_with(start="1 Jan 200 10:01", end="3 Mar 200 10:01")
        container = a_container_with(text="container")
        subevent.container = container
        self.assertEqual(container, subevent.container)

    def test_properties_defaults(self):
        subevent = a_subevent_with(start="1 Jan 200 10:01", end="3 Mar 200 10:01")
        self.assertEqual(False, subevent.get_fuzzy())
        self.assertEqual(False, subevent.get_locked())
        self.assertEqual(False, subevent.get_ends_today())
        self.assertEqual(False, subevent.is_container())
        self.assertEqual(True, subevent.is_subevent())
