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


from timelinelib.canvas.data.immutable import ImmutableCategory
from timelinelib.canvas.data.immutable import ImmutableContainer
from timelinelib.canvas.data.immutable import ImmutableDB
from timelinelib.canvas.data.immutable import ImmutableEra
from timelinelib.canvas.data.immutable import ImmutableEvent
from timelinelib.canvas.data.immutable import ImmutableMilestone
from timelinelib.canvas.data.immutable import InvalidOperationError
from timelinelib.general.immutable import ImmutableDict
from timelinelib.test.cases.unit import UnitTestCase


class DBTestCase(UnitTestCase):

    def assertDifferentIdentity(self, o1, o2):
        self.assertEqual(type(o1), type(o2))
        self.assertFalse(o1 is o2)


class describe_saving_event(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB()
        db2 = db1.save_event(ImmutableEvent(), 1)
        self.assertDifferentIdentity(db1, db2)

    def test_event_is_added(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="work"), 1)
        db = db.save_event(ImmutableEvent(text="meeting", category_id=1), 2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="work"),
            }),
            events=ImmutableDict({
                2: ImmutableEvent(text="meeting", category_id=1),
            }),
        ))

    def test_event_is_updated(self):
        db = ImmutableDB()
        db = db.save_event(ImmutableEvent(text="meeting"), 1)
        db = db.save_event(ImmutableEvent(text="lunch"), 1)
        self.assertEqual(db, ImmutableDB(
            events=ImmutableDict({
                1: ImmutableEvent(text="lunch"),
            }),
        ))

    def test_fails_if_category_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category with id 99 does not exist$",
            db.save_event, ImmutableEvent(category_id=99), 1
        )

    def test_fails_if_container_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Container with id 99 does not exist$",
            db.save_event, ImmutableEvent(container_id=99), 1
        )


class describe_deleting_event(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB().save_event(ImmutableEvent(), 1)
        db2 = db1.delete_event(1)
        self.assertDifferentIdentity(db1, db2)

    def test_event_is_removed(self):
        db = ImmutableDB()
        db = db.save_event(ImmutableEvent(text="meeting"), 1)
        db = db.save_event(ImmutableEvent(text="football"), 2)
        db = db.delete_event(1)
        self.assertEqual(db, ImmutableDB(
            events=ImmutableDict({
                2: ImmutableEvent(text="football"),
            }),
        ))

    def test_fails_if_event_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Event with id 99 does not exist$",
            db.delete_event, 99
        )


class describe_saving_category(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB()
        db2 = db1.save_category(ImmutableCategory(), 1)
        self.assertDifferentIdentity(db1, db2)

    def test_category_is_added(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="foo"), 1)
        db = db.save_category(ImmutableCategory(name="bar"), 2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="foo"),
                2: ImmutableCategory(name="bar"),
            })
        ))

    def test_category_is_updated(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="foo"), 1)
        db = db.save_category(ImmutableCategory(name="bar"), 2)
        db = db.save_category(ImmutableCategory(name="foo2"), 1)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="foo2"),
                2: ImmutableCategory(name="bar"),
            })
        ))

    def test_fails_if_name_exists(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="foo"), 1)
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category name 'foo' is not unique$",
            db.save_category, ImmutableCategory(name="foo"), 2
        )

    def test_fails_if_parent_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category with id 99 does not exist$",
            db.save_category, ImmutableCategory(parent_id=99), 1
        )

    def test_fails_if_parent_creates_circular_reference(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="root"), 1)
        db = db.save_category(ImmutableCategory(name="child", parent_id=1), 2)
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Circular category parent$",
            db.save_category, ImmutableCategory(parent_id=2), 1
        )


class describe_deleting_category(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB().save_category(ImmutableCategory(name="work"), 1)
        db2 = db1.delete_category(1)
        self.assertDifferentIdentity(db1, db2)

    def test_category_is_removed(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="work"), 1)
        db = db.save_category(ImmutableCategory(name="play"), 2)
        db = db.delete_category(1)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                2: ImmutableCategory(name="play"),
            }),
        ))

    def test_category_parent_id_attribute_is_updated(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="root"), 1)
        db = db.save_category(ImmutableCategory(name="sub", parent_id=1), 2)
        db = db.save_category(ImmutableCategory(name="child1", parent_id=2), 3)
        db = db.save_category(ImmutableCategory(name="child2", parent_id=2), 4)
        db = db.delete_category(2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="root"),
                3: ImmutableCategory(name="child1", parent_id=1),
                4: ImmutableCategory(name="child2", parent_id=1),
            }),
        ))

    def test_event_category_id_attribute_is_updated(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="root"), 1)
        db = db.save_category(ImmutableCategory(name="sub", parent_id=1), 2)
        db = db.save_event(ImmutableEvent(text="lunch", category_id=2), 3)
        db = db.save_event(ImmutableEvent(text="dinner", category_id=2), 4)
        db = db.delete_category(2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="root"),
            }),
            events=ImmutableDict({
                3: ImmutableEvent(text="lunch", category_id=1),
                4: ImmutableEvent(text="dinner", category_id=1),
            }),
        ))

    def test_milestone_category_id_attribute_is_updated(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="root"), 1)
        db = db.save_category(ImmutableCategory(name="sub", parent_id=1), 2)
        db = db.save_milestone(ImmutableMilestone(text="lunch", category_id=2), 3)
        db = db.save_milestone(ImmutableMilestone(text="dinner", category_id=2), 4)
        db = db.delete_category(2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="root"),
            }),
            milestones=ImmutableDict({
                3: ImmutableMilestone(text="lunch", category_id=1),
                4: ImmutableMilestone(text="dinner", category_id=1),
            }),
        ))

    def test_container_category_id_attribute_is_updated(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="root"), 1)
        db = db.save_category(ImmutableCategory(name="sub", parent_id=1), 2)
        db = db.save_container(ImmutableContainer(text="lunch", category_id=2), 3)
        db = db.save_container(ImmutableContainer(text="dinner", category_id=2), 4)
        db = db.delete_category(2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="root"),
            }),
            containers=ImmutableDict({
                3: ImmutableContainer(text="lunch", category_id=1),
                4: ImmutableContainer(text="dinner", category_id=1),
            }),
        ))

    def test_fails_if_category_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category with id 99 does not exist$",
            db.delete_category, 99
        )


class describe_saving_era(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB()
        db2 = db1.save_era(ImmutableEra(), 1)
        self.assertDifferentIdentity(db1, db2)

    def test_era_is_added(self):
        db = ImmutableDB()
        db = db.save_era(ImmutableEra(name="present"), 1)
        db = db.save_era(ImmutableEra(name="past"), 2)
        self.assertEqual(db, ImmutableDB(
            eras=ImmutableDict({
                1: ImmutableEra(name="present"),
                2: ImmutableEra(name="past"),
            }),
        ))

    def test_era_is_updated(self):
        db = ImmutableDB()
        db = db.save_era(ImmutableEra(name="present"), 1)
        db = db.save_era(ImmutableEra(name="past"), 1)
        self.assertEqual(db, ImmutableDB(
            eras=ImmutableDict({
                1: ImmutableEra(name="past"),
            }),
        ))


class describe_deleting_era(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB().save_era(ImmutableEra(), 1)
        db2 = db1.delete_era(1)
        self.assertDifferentIdentity(db1, db2)

    def test_era_is_removed(self):
        db = ImmutableDB()
        db = db.save_era(ImmutableEra(name="past"), 1)
        db = db.save_era(ImmutableEra(name="present"), 2)
        db = db.delete_era(1)
        self.assertEqual(db, ImmutableDB(
            eras=ImmutableDict({
                2: ImmutableEra(name="present"),
            }),
        ))

    def test_fails_if_era_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Era with id 99 does not exist$",
            db.delete_era, 99
        )


class describe_saving_milestone(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB()
        db2 = db1.save_milestone(ImmutableMilestone(), 1)
        self.assertDifferentIdentity(db1, db2)

    def test_milestone_is_added(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="work"), 1)
        db = db.save_milestone(ImmutableMilestone(text="release", category_id=1), 2)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="work"),
            }),
            milestones=ImmutableDict({
                2: ImmutableMilestone(text="release", category_id=1),
            }),
        ))

    def test_milestone_is_updated(self):
        db = ImmutableDB()
        db = db.save_milestone(ImmutableMilestone(text="release"), 1)
        db = db.save_milestone(ImmutableMilestone(text="alpha"), 1)
        self.assertEqual(db, ImmutableDB(
            milestones=ImmutableDict({
                1: ImmutableMilestone(text="alpha"),
            }),
        ))

    def test_fails_if_category_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category with id 99 does not exist$",
            db.save_milestone, ImmutableMilestone(category_id=99), 1
        )


class describe_deleting_milestone(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB().save_milestone(ImmutableMilestone(text="release"), 1)
        db2 = db1.delete_milestone(1)
        self.assertDifferentIdentity(db1, db2)

    def test_milestone_is_removed(self):
        db = ImmutableDB()
        db = db.save_milestone(ImmutableMilestone(text="release"), 1)
        db = db.save_milestone(ImmutableMilestone(text="alpha"), 2)
        db = db.delete_milestone(1)
        self.assertEqual(db, ImmutableDB(
            milestones=ImmutableDict({
                2: ImmutableMilestone(text="alpha"),
            }),
        ))

    def test_fails_if_milestone_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Milestone with id 99 does not exist$",
            db.delete_milestone, 99
        )


class describe_saving_container(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB()
        db2 = db1.save_container(ImmutableContainer(), 1)
        self.assertDifferentIdentity(db1, db2)

    def test_container_is_added(self):
        db = ImmutableDB()
        db = db.save_category(ImmutableCategory(name="work"), 1)
        db = db.save_container(ImmutableContainer(text="foo"), 2)
        db = db.save_container(ImmutableContainer(text="bar", category_id=1), 3)
        self.assertEqual(db, ImmutableDB(
            categories=ImmutableDict({
                1: ImmutableCategory(name="work"),
            }),
            containers=ImmutableDict({
                2: ImmutableContainer(text="foo"),
                3: ImmutableContainer(text="bar", category_id=1),
            })
        ))

    def test_container_is_updated(self):
        db = ImmutableDB()
        db = db.save_container(ImmutableContainer(text="foo"), 1)
        db = db.save_container(ImmutableContainer(text="bar"), 2)
        db = db.save_container(ImmutableContainer(text="bar2"), 2)
        self.assertEqual(db, ImmutableDB(
            containers=ImmutableDict({
                1: ImmutableContainer(text="foo"),
                2: ImmutableContainer(text="bar2"),
            })
        ))

    def test_fails_if_category_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Category with id 99 does not exist$",
            db.save_container, ImmutableContainer(category_id=99), 1
        )


class describe_deleting_container(DBTestCase):

    def test_db_is_not_mutated(self):
        db1 = ImmutableDB().save_container(ImmutableContainer(text="group"), 1)
        db2 = db1.delete_container(1)
        self.assertDifferentIdentity(db1, db2)

    def test_container_is_removed(self):
        db = ImmutableDB()
        db = db.save_container(ImmutableContainer(text="foo"), 1)
        db = db.save_container(ImmutableContainer(text="bar"), 2)
        db = db.delete_container(1)
        self.assertEqual(db, ImmutableDB(
            containers=ImmutableDict({
                2: ImmutableContainer(text="bar"),
            })
        ))

    def test_event_container_id_attribute_is_updated(self):
        db = ImmutableDB()
        db = db.save_container(ImmutableContainer(text="group"), 1)
        db = db.save_event(ImmutableEvent(text="lunch", container_id=1), 2)
        db = db.save_event(ImmutableEvent(text="dinner", container_id=1), 3)
        db = db.delete_container(1)
        self.assertEqual(db, ImmutableDB(
            events=ImmutableDict({
                2: ImmutableEvent(
                    text="lunch",
                    container_id=None
                ),
                3: ImmutableEvent(
                    text="dinner",
                    container_id=None
                ),
            }),
        ))

    def test_fails_if_container_does_not_exist(self):
        db = ImmutableDB()
        self.assertRaisesRegex(
            InvalidOperationError,
            r"^Container with id 99 does not exist$",
            db.delete_container, 99
        )
