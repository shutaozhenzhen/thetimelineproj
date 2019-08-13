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


import random
import subprocess

from timelinelib.dataexport.timelinexml import export_db_to_timeline_xml
from timelinelib.dataimport.tutorial import create_in_memory_gregorian_tutorial_db
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import a_container
from timelinelib.test.utils import an_event
from timelinelib.test.utils import a_time_period


class describe_undo(TmpDirTestCase):

    DIFF_PROGRAM = "diff"

    def test_a_series_of_operations_can_be_undone(self):
        db_operations = DBOperations(self.original_path, self.after_undo_path)
        db = create_in_memory_gregorian_tutorial_db()
        operation_log = db_operations.perform(db)
        if self.read(self.original_path) != self.read(self.after_undo_path):
            self.fail_with_diff(operation_log)

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.original_path = self.get_tmp_path("original.timeline")
        self.after_undo_path = self.get_tmp_path("after_undo.timeline")

    def read(self, path):
        f = open(path, "rb")
        try:
            return f.read()
        finally:
            f.close()

    def fail_with_diff(self, operation_log):
        lines = ["Operations could not be undone:"]
        lines.append("")
        for name in operation_log:
            lines.append("- %s" % name)
        lines.append("")
        lines.append("Diff (original -> after undo):")
        lines.append("")
        for line in self.get_diff().split("\n"):
            lines.append("%s" % line.strip())
        self.fail("\n".join(lines))

    def get_diff(self):
        try:
            cmd = [self.DIFF_PROGRAM, self.original_path, self.after_undo_path]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = process.communicate()[0]
        except:
            return "no diff program found"
        else:
            return output


class DBOperations(object):

    def __init__(self, original_path, after_undo_path):
        self.original_path = original_path
        self.after_undo_path = after_undo_path

    def perform(self, db):
        operation_log = []
        for _ in range(random.randint(0, 3)):
            operation_log.append(self._perform_single_until_succeeds(db))
        operation_log.append(self._operation_save_original(db))
        num_operations = random.randint(1, 5)
        for _ in range(num_operations):
            operation_log.append(self._perform_single_until_succeeds(db))
        for _ in range(num_operations):
            operation_log.append(self._operation_undo(db))
        operation_log.append(self._operation_save_after_undo(db))
        return operation_log

    def _perform_single_until_succeeds(self, db):
        while True:
            try:
                return self._get_single()(db)
            except OperationNotPossibleError:
                pass

    def _operation_save_original(self, db):
        export_db_to_timeline_xml(db, self.original_path)
        return "save original"

    def _operation_undo(self, db):
        db.undo()
        return "undo"

    def _operation_save_after_undo(self, db):
        export_db_to_timeline_xml(db, self.after_undo_path)
        return "save after undo"

    def _get_single(self):
        return random.choice([
            self._operation_change_default_color,
            self._operation_change_progress,
            self._operation_change_category,
            self._operation_add_category,
            self._operation_delete_category,
            self._operation_change_fuzzy,
            self._operation_change_ends_today,
            self._operation_change_locked,
            self._operation_change_text,
            self._operation_change_description,
            self._operation_delete_event,
            self._operation_add_event,
            self._operation_change_hyperlink,
            self._operation_change_time_period,
            self._operation_add_container_with_subevents,
        ])

    def _operation_change_default_color(self, db):
        event = self._get_random_event(db, container=False)
        while True:
            new_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            if new_color != event.get_default_color():
                event.set_default_color(new_color)
                break
        db.save_event(event)
        return "change default color to %s %r" % (new_color, event)

    def _operation_change_progress(self, db):
        event = self._get_random_event(db, container=False, milestone=False)
        while True:
            new_progress = random.randint(0, 100)
            if new_progress != event.get_progress():
                event.set_progress(new_progress)
                break
        db.save_event(event)
        return "change progress to %s %r" % (new_progress, event)

    def _operation_change_category(self, db):
        event = self._get_random_event(db, container=False)
        category = self._get_random_category(db, exclude=event.get_category())
        event.set_category(category)
        db.save_event(event)
        return "change category to %r %r" % (category, event)

    def _operation_delete_category(self, db):
        category = self._get_random_category(db)
        db.delete_category(category)
        return "delete category %r" % category

    def _operation_add_category(self, db):
        counter = 0
        while True:
            counter += 1
            name = "new category %d" % counter
            if db.get_category_by_name(name) is None:
                category = a_category_with(name=name)
                break
        db.save_category(category)
        return "save category %r" % category

    def _operation_change_fuzzy(self, db):
        event = self._get_random_event(db, container=False, milestone=False)
        event.set_fuzzy(not event.get_fuzzy())
        db.save_event(event)
        return "change fuzzy to %s %r" % (event.get_fuzzy(), event)

    def _operation_change_ends_today(self, db):
        event = self._get_random_event(
            db,
            container=False,
            subevent=False,
            milestone=False
        )
        event.set_ends_today(not event.get_ends_today())
        db.save_event(event)
        return "change ends-today to %s %r" % (event.get_ends_today(), event)

    def _operation_change_locked(self, db):
        event = self._get_random_event(
            db,
            container=False,
            subevent=False,
            milestone=False
        )
        event.set_locked(not event.get_locked())
        db.save_event(event)
        return "change locked to %s %r" % (event.get_locked(), event)

    def _operation_change_text(self, db):
        event = self._get_random_event(db, container=False)
        event.set_text(self._get_random_string(4, 16))
        db.save_event(event)
        return "change text to %s %r" % (event.get_text(), event)

    def _operation_change_description(self, db):
        event = self._get_random_event(db, container=False)
        event.set_description(self._get_random_string(24, 36))
        db.save_event(event)
        return "change description to %s %r" % (event.get_description(), event)

    def _operation_delete_event(self, db):
        event = self._get_random_event(db)
        db.delete_event(event)
        return "deleted event %r" % (event)

    def _operation_add_event(self, db):
        event = an_event()
        db.save_event(event)
        return "added event %r" % (event)

    def _operation_change_hyperlink(self, db):
        event = self._get_random_event(db, container=False, milestone=False)
        event.set_hyperlink("http://%s" % self._get_random_string(2, 7))
        db.save_event(event)
        return "changed hyperlink to %s %r" % (event.get_hyperlink(), event)

    def _operation_change_time_period(self, db):
        event = self._get_random_event(db, container=False, milestone=False)
        event.set_time_period(a_time_period())
        db.save_event(event)
        return "changed time_period to %s %r" % (db.get_time_type().format_period(event.get_time_period()), event)

    def _operation_add_container_with_subevents(self, db):
        all_events = a_container("Container", None, [("sub1", None), ("sub2", None)])
        db.save_events(all_events)
        return "added a container with subevents %r" % (all_events[0])

    def _get_random_string(self, min_length, max_length):
        import string
        return ''.join(random.choice(string.ascii_lowercase + "     ") for _ in range(random.randint(min_length, max_length)))

    def _get_random_event(self, db, regular=True, subevent=True,
                          container=True, milestone=True):
        possible_events = []
        for event in db.get_all_events():
            if event.is_container():
                if container:
                    possible_events.append(event)
            elif event.is_subevent():
                if subevent:
                    possible_events.append(event)
            elif event.is_milestone():
                if milestone:
                    possible_events.append(event)
            else:
                if regular:
                    possible_events.append(event)
        if len(possible_events) == 0:
            raise OperationNotPossibleError()
        return random.choice(possible_events)

    def _get_random_category(self, db, exclude=None):
        possible_categories = [category for category in db.get_categories()
                               if category != exclude]
        if len(possible_categories) == 0:
            raise OperationNotPossibleError()
        return random.choice(possible_categories)


class OperationNotPossibleError(Exception):
    pass
