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

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.exceptions import TimelineIOError
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import a_container
from timelinelib.test.utils import a_container_with
from timelinelib.test.utils import a_gregorian_era
from timelinelib.test.utils import a_gregorian_era_with
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import a_subevent_with
from timelinelib.test.utils import gregorian_period
from timelinelib.repositories.dbwrapper import category_tree


class describe_memory_db(UnitTestCase):

    def testInitialState(self):
        db = MemoryDB()
        self.assertEqual(db.path, "")
        self.assertEqual(db.displayed_period, None)
        self.assertEqual(db.get_hidden_categories(), [])
        self.assertEqual(db.is_read_only(), False)
        self.assertEqual(db.search(""), [])
        self.assertEqual(db.get_all_events(), [])
        self.assertEqual(db.get_first_event(), None)
        self.assertEqual(db.get_last_event(), None)
        self.assertEqual(db.get_categories(), [])

    def testLoadSaveViewProperties(self):
        # Make sure the database contains categories
        self.db.save_category(self.c1)
        self.db.save_category(self.c2)
        # Set up a view properties object that simulates having selected a
        # specific period and hidden one category
        vp = ViewProperties()
        vp.set_category_visible(self.c1, False)
        tp = gregorian_period("23 Mar 2010", "24 Mar 2010")
        vp.displayed_period = tp
        # Save these properties and assert that the database fields are written
        # correctly
        self.db.save_view_properties(vp)
        self.assertEqual(self.db.displayed_period, tp)
        self.assertEqual(self.db.get_hidden_categories(), [self.c1])
        # Load view properties from db simulating that this db was just loaded
        # into memory and the view is being configured
        new_vp = ViewProperties()
        self.db.load_view_properties(new_vp)
        self.assertFalse(new_vp.is_category_visible(self.c1))
        self.assertTrue(new_vp.is_category_visible(self.c2))
        self.assertEqual(new_vp.displayed_period, self.db.displayed_period)
        # Assert save called: 2 save categories, 1 save view properties
        self.assertEqual(self.save_callback_mock.call_count, 3)

    def testSaveInvalidDisplayedPeriod(self):
        # Assign a zero-period as displayed period
        vp = ViewProperties()
        tp = gregorian_period("23 Mar 2010", "23 Mar 2010")
        vp.displayed_period = tp
        # Assert error when trying to save
        self.assertRaises(TimelineIOError, self.db.save_view_properties, vp)

    def testGetSetDisplayedPeriod(self):
        tp = gregorian_period("23 Mar 2010", "24 Mar 2010")
        self.db.set_displayed_period(tp)
        # Assert that we get back the same period
        self.assertEqual(self.db.get_displayed_period(), tp)
        # Assert that the period is correctly loaded into ViewProperties
        vp = ViewProperties()
        self.db.load_view_properties(vp)
        self.assertEqual(vp.displayed_period, tp)

    def testGetSetHiddenCategories(self):
        # Assert that we cannot include categories not in the db
        self.assertRaises(ValueError, self.db.set_hidden_categories, [self.c1])
        self.db.set_hidden_categories([])
        self.db.save_category(self.c1)
        self.db.save_category(self.c2)
        self.db.set_hidden_categories([self.c1])
        # Assert that the returned list is the same
        self.assertEqual(self.db.get_hidden_categories(), [self.c1])
        # Assert that category visibility information is correctly written to
        # ViewProperties
        vp = ViewProperties()
        self.db.load_view_properties(vp)
        self.assertFalse(vp.is_category_visible(self.c1))
        self.assertTrue(vp.is_category_visible(self.c2))

    def testSaveNewCategory(self):
        self.db.save_category(self.c1)
        self.assertTrue(self.c1.has_id())
        self.assertEqual(self.db.get_categories(), [self.c1])
        self.assertEqual(self.db_listener.call_count, 1)
        # Assert save called: 1 save category
        self.assertEqual(self.save_callback_mock.call_count, 1)

    def testSaveExistingCategory(self):
        self.db.save_category(self.c1)
        id_before = self.c1.get_id()
        self.c1.set_name("new name")
        self.db.save_category(self.c1)
        self.assertEqual(id_before, self.c1.get_id())
        self.assertEqual(self.db.get_categories(), [self.c1])
        self.assertEqual(self.db_listener.call_count, 2)  # 2 save
        # Assert save called: 2 save category
        self.assertEqual(self.save_callback_mock.call_count, 2)

    def testSaveNonExistingCategory(self):
        other_db = MemoryDB()
        other_db.save_category(self.c1)
        # It has id but is not in this db
        self.assertRaises(TimelineIOError, self.db.save_category, self.c1)
        # Assert save not called
        self.assertEqual(self.save_callback_mock.call_count, 0)

    def testSaveCategoryWithUnknownParent(self):
        self.c1.set_parent(self.c2)
        # c2 not in db so we should get exception
        self.assertRaises(TimelineIOError, self.db.save_category, self.c1)
        # But after c2 is added everything is fine
        self.db.save_category(self.c2)
        self.db.save_category(self.c1)

    def testSaveCategoryWithParentChange(self):
        # Start with this hierarchy:
        # c1
        #   c11
        #     c111
        #   c12
        c1 = a_category_with(name="c1", parent=None)
        c11 = a_category_with(name="c11", parent=c1)
        c111 = a_category_with(name="c111", parent=c11)
        c12 = a_category_with(name="c12", parent=c1)
        self.db.save_category(c1)
        self.db.save_category(c11)
        self.db.save_category(c111)
        self.db.save_category(c12)
        # Changing c11's parent to c12 should create the following tree:
        # c1
        #   c12
        #     c11
        #       c111
        c11.set_parent(c12)
        self.db.save_category(c11)
        self.assertEqual(c1._get_parent(), None)
        self.assertEqual(c12._get_parent(), c1)
        self.assertEqual(c11._get_parent(), c12)
        self.assertEqual(c111._get_parent(), c11)
        # Changing c11's parent to c111 should raise exception since that would
        # create a circular parent link.
        c11.set_parent(c111)
        self.assertRaises(TimelineIOError, self.db.save_category, c11)

    def testDeleteExistingCategory(self):
        # Add two categories to the db
        self.db.save_category(self.c1)
        self.db.save_category(self.c2)
        # Make category 1 hidden
        vp = ViewProperties()
        vp.set_category_visible(self.c1, False)
        self.db.save_view_properties(vp)
        # Assert both categories in db
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 2)
        self.assertTrue(self.c1 in categories)
        self.assertTrue(self.c2 in categories)
        # Remove first (by category)
        self.db.delete_category(self.c1)
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 1)
        self.assertTrue(self.c2 in categories)
        self.assertFalse(self.c1.has_id())
        self.assertFalse(self.c1 in self.db.get_hidden_categories())
        # Remove second (by id)
        self.db.delete_category(self.c2.get_id())
        categories = self.db.get_categories()
        self.assertEqual(len(categories), 0)
        # Check events
        self.assertEqual(self.db_listener.call_count, 4)  # 2 save, 2 delete
        # Assert save called: 2 save category, 1 save view
        # properties, 2 delete categories
        self.assertEqual(self.save_callback_mock.call_count, 5)

    def testDeleteNonExistingCategory(self):
        self.assertRaises(TimelineIOError, self.db.delete_category, self.c1)
        self.assertRaises(TimelineIOError, self.db.delete_category, 5)
        other_db = MemoryDB()
        other_db.save_category(self.c2)
        self.assertRaises(TimelineIOError, self.db.delete_category, self.c2)
        # Assert save not called
        self.assertEqual(self.save_callback_mock.call_count, 0)

    def testDeleteCategoryWithParent(self):
        # Create hierarchy:
        # c1
        #   c11
        #   c12
        #     c121
        c1 = a_category_with(name="c1", parent=None)
        c11 = a_category_with(name="c11", parent=c1)
        c12 = a_category_with(name="c12", parent=c1)
        c121 = a_category_with(name="c121", parent=c12)
        self.db.save_category(c1)
        self.db.save_category(c11)
        self.db.save_category(c12)
        self.db.save_category(c121)
        # Delete c12 should cause c121 to get c1 as parent
        self.db.delete_category(c12)
        self.assertEqual(c121.reload().parent, c1)
        # Delete c1 should cause c11, and c121 to be parentless
        self.db.delete_category(c1)
        self.assertEqual(c11.reload().parent, None)
        self.assertEqual(c121.reload().parent, None)

    def testDeleteCategoryWithEvent(self):
        # Create hierarchy:
        # c1
        #   c11
        c1 = a_category_with(name="c1", parent=None)
        c11 = a_category_with(name="c11", parent=c1)
        self.db.save_category(c1)
        self.db.save_category(c11)
        # Create event belonging to c11
        self.e1.category = c11
        self.db.save_event(self.e1)
        # Delete c11 should cause e1 to get c1 as category
        self.db.delete_category(c11)
        self.assertEqual(self.e1.reload().category, c1)
        # Delete c1 should cause e1 to have no category
        self.db.delete_category(c1)
        self.assertEqual(self.e1.reload().category, None)

    def testSaveEventUnknownCategory(self):
        # A new
        self.e1.set_category(self.c1)
        self.assertRaises(TimelineIOError, self.db.save_event, self.e1)
        # An existing
        self.db.save_event(self.e2)
        self.e2.set_category(self.c1)
        self.assertRaises(TimelineIOError, self.db.save_event, self.e2)
        # Assert save not called
        self.assertEqual(self.save_callback_mock.call_count, 1)

    def testSaveNewEvent(self):
        self.db.save_event(self.e1)
        tp = gregorian_period("12 Feb 2010", "14 Feb 2010")
        self.assertTrue(self.e1.has_id())
        self.assertEqual(self.db.get_events(tp), [self.e1])
        self.assertEqual(self.db.get_all_events(), [self.e1])
        self.assertEqual(self.db_listener.call_count, 1)  # 1 save
        # Assert save called: 1 save event
        self.assertEqual(self.save_callback_mock.call_count, 1)

    def testSaveExistingEvent(self):
        self.db.save_event(self.e1)
        id_before = self.e1.get_id()
        self.e1.set_text("new text")
        self.db.save_event(self.e1)
        tp = gregorian_period("12 Feb 2010", "14 Feb 2010")
        self.assertEqual(id_before, self.e1.get_id())
        self.assertEqual(self.db.get_events(tp), [self.e1])
        self.assertEqual(self.db.get_all_events(), [self.e1])
        self.assertEqual(self.db_listener.call_count, 2)  # 1 save
        # Assert save called: 2 save event
        self.assertEqual(self.save_callback_mock.call_count, 2)

    def testSaveNonExistingEvent(self):
        other_db = MemoryDB()
        other_db.save_event(self.e1)
        # It has id but is not in this db
        self.assertRaises(TimelineIOError, self.db.save_event, self.e1)
        # Assert save not called
        self.assertEqual(self.save_callback_mock.call_count, 0)

    def testDeleteExistingEvent(self):
        tp = gregorian_period("12 Feb 2010", "15 Feb 2010")
        self.db.save_event(self.e1)
        self.db.save_event(self.e2)
        # Assert both in db
        self.assertEqual(len(self.db.get_events(tp)), 2)
        self.assertTrue(self.e1 in self.db.get_events(tp))
        self.assertTrue(self.e2 in self.db.get_events(tp))
        # Delete first (by event)
        self.db.delete_event(self.e1)
        self.assertFalse(self.e1.has_id())
        self.assertEqual(len(self.db.get_events(tp)), 1)
        self.assertTrue(self.e2 in self.db.get_events(tp))
        # Delete second (by id)
        self.db.delete_event(self.e2.get_id())
        self.assertEqual(len(self.db.get_events(tp)), 0)
        # Check events
        self.assertEqual(self.db_listener.call_count, 4)  # 2 save, 2 delete
        # Assert save called: 2 save event, 2 delete event
        self.assertEqual(self.save_callback_mock.call_count, 4)

    def testDeleteNonExistingEvent(self):
        self.assertRaises(TimelineIOError, self.db.delete_event, self.e1)
        self.assertRaises(TimelineIOError, self.db.delete_event, 5)
        other_db = MemoryDB()
        other_db.save_event(self.e2)
        self.assertRaises(TimelineIOError, self.db.delete_event, self.e2)
        # Assert save not called
        self.assertEqual(self.save_callback_mock.call_count, 0)

    def testEventShouldNotBeFuzzyByDefault(self):
        self.assertFalse(self.e1.get_fuzzy())

    def testEventShouldNotBeLockedByDefault(self):
        self.assertFalse(self.e1.get_locked())

    def setUp(self):
        self.save_callback_mock = Mock()
        self.db = MemoryDB()
        self.db.register_save_callback(self.save_callback_mock)
        self.db_listener = Mock()
        self.c1 = a_category_with(name="work")
        self.c2 = a_category_with(name="private")
        self.e1 = an_event_with(text="holiday", time="13 Feb 2010")
        self.e2 = an_event_with(text="work starts", time="13 Feb 2010")
        self.e3 = an_event_with(text="period", time="13 Feb 2010")
        self.db.register(self.db_listener)


class describe_querying(UnitTestCase):

    def test_can_get_first_event(self):
        aug_event = an_event_with(time="30 Aug 2010")
        jan_event = an_event_with(time="1 Jan 2010")
        self.db.save_event(aug_event)
        self.db.save_event(jan_event)
        self.assertEqual(self.db.get_first_event(), jan_event)

    def test_can_get_last_event(self):
        jan_event = an_event_with(time="1 Jan 2010")
        aug_event = an_event_with(time="30 Aug 2010")
        self.db.save_event(aug_event)
        self.db.save_event(jan_event)
        self.assertEqual(self.db.get_last_event(), aug_event)

    def test_can_get_subevents(self):
        self.db.save_events(
            a_container(name="con", category=None, sub_events=[
                ("sub1", None),
            ])
        )
        all_events = self.db.get_all_events()
        containers = [e.text for e in all_events if e.is_container()]
        subevents = [e.text for e in all_events if e.is_subevent()]
        self.assertEqual((containers, subevents), (["con"], ["sub1"]))

    def setUp(self):
        self.db = MemoryDB()


class describe_searching(UnitTestCase):

    def test_find_events_with_matching_text(self):
        holiday_event = an_event_with(text="holiday in the alps")
        football_event = an_event_with(text="football training")
        self.db.save_event(holiday_event)
        self.db.save_event(football_event)
        self.assertEqual(self.db.search("holiday"), [holiday_event])

    def setUp(self):
        self.db = MemoryDB()


class describe_undo(UnitTestCase):

    def test_undo_enabled(self):
        self.assertFalse(self.db.undo_enabled())
        self.db.save_event(an_event_with())
        self.assertTrue(self.db.undo_enabled())

    def test_redo_enabled(self):
        self.assertFalse(self.db.redo_enabled())
        self.db.save_event(an_event_with())
        self.db.undo()
        self.assertTrue(self.db.redo_enabled())

    def test_can_not_undo_non_modified_timeline(self):
        self.db.undo()
        self.assertFalse(self.db_changed_listener.called)

    def test_can_undo_added_event(self):
        self.db.save_event(an_event_with(text="football"))
        self.assertHasEvents(["football"])
        self.db.undo()
        self.assertHasEvents([])

    def test_can_redo_undo(self):
        self.db.save_event(an_event_with(text="football"))
        self.assertHasEvents(["football"])
        self.db.undo()
        self.assertHasEvents([])
        self.db.redo()
        self.assertHasEvents(["football"])

    def assertHasEvents(self, event_texts):
        actual_event_texts = [e.get_text() for e in self.db.get_all_events()]
        self.assertEqual(actual_event_texts, event_texts)

    def setUp(self):
        self.db_changed_listener = Mock()
        self.db = MemoryDB()
        self.db.listen_for_any(self.db_changed_listener)


class describe_importing(UnitTestCase):

    def test_importing_empty_db_does_nothing(self):
        self.base_db.import_db(self.import_db)
        self.assertEqual(self.base_db.get_categories(), [])
        self.assertEqual(self.base_db.get_all_events(), [])

    def test_events_are_imported(self):
        self.import_db.save_event(an_event_with(text="dentist"))
        self.import_db.save_event(an_event_with(text="golf"))
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "dentist ()",
            "golf ()",
        ])

    def test_subevents_are_imported(self):
        category = self.import_db.new_category(name="cat").save()
        container = self.import_db.new_container(text="cont").save()
        self.import_db.new_subevent(text="sub1", container=container).save()
        self.import_db.new_subevent(text="sub2", category=category, container=container).save()
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "cont () [sub1 (), sub2 (cat)]",
        ])

    def test_events_are_imported_into_existing_categories(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_event(an_event_with(
            text="dentist",
            category=self.import_db.get_category_by_name("work")))
        self.base_db.save_category(a_category_with(name="work"))
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "dentist (work)",
        ])
        self.assertCategoryTreeIs([
            ("work", [])
        ])

    def test_new_categories_are_created_if_they_do_not_exist(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_event(an_event_with(
            text="dentist",
            category=self.import_db.get_category_by_name("work")))
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "dentist (work)",
        ])
        self.assertCategoryTreeIs([
            ("work", [])
        ])

    def test_new_categories_preserve_parent(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_category(a_category_with(
            name="paper work",
            parent=self.import_db.get_category_by_name("work")))
        self.import_db.save_event(an_event_with(
            text="write article",
            category=self.import_db.get_category_by_name("paper work")))
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "write article (paper work)",
        ])
        self.assertCategoryTreeIs([
            ("work", [
                ("paper work", []),
            ])
        ])

    def test_new_categories_are_attached_to_existing_ones(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_category(a_category_with(
            name="paper work",
            parent=self.import_db.get_category_by_name("work")))
        self.import_db.save_event(an_event_with(
            text="write article",
            category=self.import_db.get_category_by_name("paper work")))
        self.base_db.save_category(a_category_with(name="work"))
        self.base_db.import_db(self.import_db)
        self.assertEventListIs([
            "write article (paper work)",
        ])
        self.assertCategoryTreeIs([
            ("work", [
                ("paper work", []),
            ])
        ])

    def test_categories_without_events_are_not_imported(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_category(a_category_with(
            name="paper work",
            parent=self.import_db.get_category_by_name("work")))
        self.base_db.import_db(self.import_db)
        self.assertCategoryTreeIs([])

    def test_save_is_only_called_once(self):
        self.import_db.save_category(a_category_with(name="work"))
        self.import_db.save_category(a_category_with(name="private"))
        self.base_db.import_db(self.import_db)
        self.assertEqual(self.base_db_save_callback.call_count, 1)

    def test_fails_if_type_type_missmatch(self):
        self.import_db.set_time_type(Mock())
        self.assertRaises(Exception, self.base_db.import_db, self.import_db)

    def assertCategoryTreeIs(self, expected_tree):
        tree = category_tree(self.base_db.get_categories())
        self.assertEqual(replace_category_with_name(tree), expected_tree)

    def assertEventListIs(self, expected_list):
        def format_event(event):
            parts = []
            parts.append("%s" % event.get_text())
            parts.append("(%s)" % category_name(event))
            if event.is_container():
                parts.append("[%s]" % ", ".join(
                    format_event(subevent)
                    for subevent
                    in event.subevents
                ))
            return " ".join(parts)
        def category_name(event):
            if event.get_category():
                return event.get_category().get_name()
            else:
                return ""
        actual_list = [
            format_event(event)
            for event
            in self.base_db.get_all_events()
            if not event.is_subevent()
        ]
        self.assertEqual(sorted(actual_list), expected_list)

    def setUp(self):
        self.base_db_save_callback = Mock()
        self.base_db = MemoryDB()
        self.base_db.register_save_callback(self.base_db_save_callback)
        self.import_db_save_callback = Mock()
        self.import_db = MemoryDB()
        self.import_db.register_save_callback(self.import_db_save_callback)


class describe_moving_events(UnitTestCase):

    def test_place_after(self):
        self.db.place_event_after_event(self.e1, self.e2)
        self.assertEventOrderIs([
            self.e2,
            self.e1,
            self.e3,
        ])

    def test_place_after_to_end(self):
        self.db.place_event_after_event(self.e1, self.e3)
        self.assertEventOrderIs([
            self.e2,
            self.e3,
            self.e1,
        ])

    def test_place_after_when_already_after(self):
        self.db.place_event_after_event(self.e3, self.e1)
        self.assertEventOrderIs([
            self.e1,
            self.e2,
            self.e3,
        ])

    def test_place_after_when_same(self):
        self.db.place_event_after_event(self.e2, self.e2)
        self.assertEventOrderIs([
            self.e1,
            self.e2,
            self.e3,
        ])

    def test_place_before(self):
        self.db.place_event_before_event(self.e2, self.e1)
        self.assertEventOrderIs([
            self.e2,
            self.e1,
            self.e3,
        ])

    def test_place_before_to_beginning(self):
        self.db.place_event_before_event(self.e3, self.e1)
        self.assertEventOrderIs([
            self.e3,
            self.e1,
            self.e2,
        ])

    def test_place_before_when_already_before(self):
        self.db.place_event_before_event(self.e1, self.e3)
        self.assertEventOrderIs([
            self.e1,
            self.e2,
            self.e3,
        ])

    def test_place_before_when_same(self):
        self.db.place_event_before_event(self.e2, self.e2)
        self.assertEventOrderIs([
            self.e1,
            self.e2,
            self.e3,
        ])

    def assertEventOrderIs(self, expected_events):
        # Check both get_all_events and get_events to ensure they are sorted
        all_event_texts = [
            event.text for event in self.db.get_all_events()
        ]
        whole_period_event_texts = [
            event.text for event in self.db.get_events(self.whole_period)
        ]
        expected_event_texts = [
            event.text for event in expected_events
        ]
        self.assertEqual(all_event_texts, whole_period_event_texts)
        self.assertEqual(whole_period_event_texts, expected_event_texts)

    def setUp(self):
        self.db = MemoryDB()
        self.e1 = an_event_with(text="e1")
        self.e2 = an_event_with(text="e2")
        self.e3 = an_event_with(text="e3")
        self.whole_period = self.e1.time_period  # All events have same period
        self.db.save_event(self.e1)
        self.db.save_event(self.e2)
        self.db.save_event(self.e3)
        self.assertEventOrderIs([
            self.e1,
            self.e2,
            self.e3,
        ])


class describe_query(UnitTestCase):

    def test_get_container(self):
        container = self.db.find_event_with_id(self.container.id)
        # Check that it loads the container
        self.assertEqual(container.text, "container")
        # Check that it loads all subevents
        self.assertEqual(
            [subevent.text for subevent in container.subevents],
            ["sub1", "sub2"]
        )
        # Check that the subevents refer to the same container
        for subevent in container.subevents:
            self.assertEqual(id(subevent.container), id(container))

    def test_get_subevent(self):
        sub1, sub2 = self.db.find_event_with_ids([self.sub1.id, self.sub2.id])
        # Check that it loads the subevents
        self.assertEqual(sub1.text, "sub1")
        self.assertEqual(sub2.text, "sub2")
        # Check that it loads the same container
        self.assertTrue(sub1.container is sub2.container)
        self.assertEqual(sub1.container.text, "container")
        # Check that it loads the same category
        self.assertTrue(sub1.category is sub2.category)
        self.assertEqual(sub1.category.name, "category")
        # Check that the subevents are referred to by the container
        self.assertEqual(
            [id(subevent) for subevent in sub1.container.subevents],
            [id(sub1), id(sub2)]
        )

    def setUp(self):
        self.db = MemoryDB()
        self.container = self.db.new_container(
            text="container"
        ).save()
        self.category = self.db.new_category(
            name="category"
        ).save()
        self.sub1 = self.db.new_subevent(
            text="sub1",
            category=self.category,
            container=self.container
        ).save()
        self.sub2 = self.db.new_subevent(
            text="sub2",
            category=self.category,
            container=self.container
        ).save()


class describe_eras(UnitTestCase):

    def test_save(self):
        self.assertEqual(len(self.db.get_all_eras()), 0)
        self.db.save_era(a_gregorian_era())
        self.assertEqual(len(self.db.get_all_eras()), 1)

    def test_delete(self):
        self.db.save_era(a_gregorian_era())
        all_eras = self.db.get_all_eras()
        self.assertEqual(len(all_eras), 1)
        self.db.delete_era(all_eras[0])
        self.assertEqual(len(self.db.get_all_eras()), 0)

    def test_retains_ends_today(self):
        self.db.save_era(a_gregorian_era_with(ends_today=True))
        self.assertEqual(self.db.get_all_eras()[0].ends_today(), True)

    def setUp(self):
        self.db = MemoryDB()


def replace_category_with_name(tree):
    return [(category.get_name(), replace_category_with_name(child_tree))
            for (category, child_tree) in tree]
