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


from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with, a_container, a_category_with


class Base(UnitTestCase):

    def setUp(self):
        self.view_properties = ViewProperties()
        self.id_counter = 0

    def create_category(self, name, parent=None):
        category = a_category_with(name=name, parent=parent)
        category.set_id(self.new_id())
        return category

    def new_id(self):
        self.id_counter += 1
        return self.id_counter


class describe_category_visibility(Base):

    def test_visible_by_default(self):
        work = self.create_category("Work", parent=None)
        self.assertTrue(self.view_properties.is_category_visible(work))

    def test_can_set_visibility(self):
        work = self.create_category("Work", parent=None)
        self.view_properties.set_category_visible(work, True)
        self.assertTrue(self.view_properties.is_category_visible(work))
        self.view_properties.set_category_visible(work, False)
        self.assertFalse(self.view_properties.is_category_visible(work))


class describe_event_visiblity(Base):

    def setUp(self):
        Base.setUp(self)
        self.work = self.create_category("Work", parent=None)
        self.meetings = self.create_category("Meetings", parent=self.work)
        self.fun_meetings = self.create_category("Fun meetings", parent=self.meetings)
        self.boring_meetings = self.create_category("Boring meetings", parent=self.meetings)

    def assertEventWithCategoryVisible(self, category):
        self.assertTrue(self.view_properties.is_event_with_category_visible(category))

    def assertEventWithCategoryHidden(self, category):
        self.assertFalse(self.view_properties.is_event_with_category_visible(category))

    def test_visible_by_default(self):
        self.assertEventWithCategoryVisible(self.boring_meetings)

    def test_visible_if_no_category(self):
        self.assertEventWithCategoryVisible(None)

    def test_visible_if_no_category_and_individual_view(self):
        self.view_properties.view_cats_individually = True
        self.assertEventWithCategoryVisible(None)

    def test_children_hidden_if_parent_hidden(self):
        self.view_properties.set_category_visible(self.work, False)
        self.assertEventWithCategoryHidden(self.boring_meetings)

    def test_children_visible_if_parent_hidden_and_individual_view(self):
        self.view_properties.view_cats_individually = True
        self.view_properties.set_category_visible(self.work, False)
        self.assertEventWithCategoryVisible(self.boring_meetings)


class describe_event_filtering(Base):

    def setUp(self):
        Base.setUp(self)
        self.work = self.create_category("Work", parent=None)
        self.play = self.create_category("Play", parent=None)
        self.write_report = self.create_event("Write report", category=self.work)
        self.play_football = self.create_event("Play football", category=self.play)

    def create_event(self, text, category):
        event = an_event_with(text=text, category=category)
        event.set_id(self.new_id())
        return event

    def test_none_filtered_by_default(self):
        events = [self.write_report, self.play_football]
        self.assertEqual(self.view_properties.filter_events(events), events)

    def test_filters_those_in_hidden_categories(self):
        self.view_properties.set_category_visible(self.play, False)
        events = [self.write_report, self.play_football]
        self.assertEqual(self.view_properties.filter_events(events),
                         [self.write_report])

    def test_filters_those_hidden_in_containers(self):
        events = a_container("Container", category=self.work, sub_events=[
            ("Write report", self.work),
            ("Play footbal", self.play),
        ])
        self.assertEqual(self.view_properties.filter_events(events), events)
        self.view_properties.set_category_visible(self.play, False)
        self.assertEqual(self.view_properties.filter_events(events), [events[0], events[1]])

    def test_filters_those_in_hidden_containers(self):
        events = a_container("Container", category=self.work, sub_events=[
            ("Write report", self.work),
            ("Play footbal", self.play),
        ])
        self.assertEqual(self.view_properties.filter_events(events), events)
        self.view_properties.set_category_visible(self.work, False)
        self.assertEqual(self.view_properties.filter_events(events), [])


class describe_highlight(Base):

    def test_can_add_highlight_to_events(self):
        self.assertFalse(self.view_properties.is_highlighted(self.event1))
        self.assertFalse(self.view_properties.is_highlighted(self.event2))
        self.assertFalse(self.view_properties.has_higlights())
        self.view_properties.add_highlight(self.event1, clear=False)
        self.view_properties.add_highlight(self.event2, clear=False)
        self.assertTrue(self.view_properties.is_highlighted(self.event1))
        self.assertTrue(self.view_properties.is_highlighted(self.event2))
        self.assertTrue(self.view_properties.has_higlights())

    def test_can_clear_when_adding_highlight_to_event(self):
        self.view_properties.add_highlight(self.event1, clear=False)
        self.view_properties.add_highlight(self.event2, clear=True)
        self.assertFalse(self.view_properties.is_highlighted(self.event1))
        self.assertTrue(self.view_properties.is_highlighted(self.event2))

    def test_can_tick_highlights(self):
        self.view_properties.add_highlight(self.event1, clear=False)
        self.assertEqual(
            self.view_properties.get_highlight_count(self.event1),
            0
        )
        self.view_properties.tick_highlights(10)
        self.assertEqual(
            self.view_properties.get_highlight_count(self.event1),
            1
        )

    def test_tick_removes_highlight_when_limit_is_passed(self):
        self.view_properties.add_highlight(self.event1, clear=False)
        self.assertEqual(
            self.view_properties.get_highlight_count(self.event1),
            0
        )
        self.view_properties.tick_highlights(5)
        self.view_properties.tick_highlights(5)
        self.view_properties.tick_highlights(5)
        self.view_properties.tick_highlights(5)
        self.view_properties.tick_highlights(5)
        self.view_properties.tick_highlights(5)
        self.assertFalse(self.view_properties.is_highlighted(self.event1))

    def test_clear_db_specific_removes_highligt(self):
        self.view_properties.add_highlight(self.event1, clear=False)
        self.assertTrue(self.view_properties.is_highlighted(self.event1))
        self.view_properties.clear_db_specific()
        self.assertFalse(self.view_properties.is_highlighted(self.event1))

    def setUp(self):
        Base.setUp(self)
        self.event1 = an_event_with(text="1")
        self.event1.set_id(self.new_id())
        self.event2 = an_event_with(text="2")
        self.event2.set_id(self.new_id())
