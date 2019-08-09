# -*- coding: utf-8 -*-
#
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


import os

from unittest.mock import Mock

from timelinelib.calendar.num.timetype import NumTimeType
from timelinelib.canvas.data.event import Event
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.importevents.controller import ImportEventsDialogController
from timelinelib.wxgui.dialogs.importevents.view import ImportEventsDialog


class describe_import_events_dialog_controller(UnitTestCase):

    def setUp(self):
        self.db = Mock()
        self.view = Mock(ImportEventsDialog)
        self.controller = ImportEventsDialogController(self.view)
        self.controller._db = self.db
        self.path = None

    def tearDown(self):
        self.remove_file()

    def create_file(self, path):
        self.path = path
        f = open(path, "w")
        f.write("Dummy")
        f.close()

    def remove_file(self):
        if self.path is not None and os.path.exists(self.path):
            os.remove(self.path)

    def test_on_filepath_changed_invalid_path_generates_error_message(self):
        self.view.GetFilePath.return_value = "\n"
        event = Mock(Event)
        self.controller.on_file_path_changed(event)
        self.view.SetError.assert_called_with(u"⟪File does not exist.⟫")
        self.assertEqual(self.controller._db_to_import, None)

    def test_on_filepath_changed_with_non_timeline_file_generates_error_message(self):
        path = ".\\dummy.txt"
        self.create_file(path)
        self.view.GetFilePath.return_value = path
        event = Mock(Event)
        self.controller.on_file_path_changed(event)
        self.view.SetError.assert_called_with(
            u"⟪Unable to load events: ⟪Unable to open timeline '.\\dummy.txt'.⟫\n\n⟪Unknown format.⟫.⟫"
        )
        self.assertEqual(self.controller._db_to_import, None)

    def test_on_filepath_changed_different_timeline_timetypes_generates_error_message(self):
        self.db.get_time_type.return_value = None
        self.view.GetFilePath.return_value = ":tutorial:"
        event = Mock(Event)
        self.controller.on_file_path_changed(event)
        self.view.SetError.assert_called_with(
            u"⟪The selected timeline has a different time type.⟫"
        )

    def test_on_filepath_changed_ok_generates_success_message(self):
        self.db.get_time_type.return_value = NumTimeType()
        self.view.GetFilePath.return_value = ":numtutorial:"
        event = Mock(Event)
        self.controller.on_file_path_changed(event)
        self.view.SetSuccess.assert_called_with(
            u"⟪17 events will be imported.⟫"
        )
        self.assertTrue(self.controller._db_to_import is not None)

    def test_on_ok_clicked_and_no_db(self):
        event = Mock(Event)
        self.controller._db_to_import = None
        self.assertEqual(self.controller.on_ok_clicked(event), None)

    def test_on_ok_clicked_db_is_imported(self):
        event = Mock(Event)
        db_to_import = Mock()
        self.controller._db_to_import = db_to_import
        self.controller.on_ok_clicked(event)
        self.controller._db.import_db.assert_called_with(db_to_import)
        self.view.Close.assert_called_with()
