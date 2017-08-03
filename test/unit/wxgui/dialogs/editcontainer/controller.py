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


from mock import Mock

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.db import db_open
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.dialogs.editcontainer.controller import EditContainerDialogController
from timelinelib.wxgui.dialogs.editcontainer.view import EditContainerDialog


class describe_edit_container_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        self.show_dialog(
            EditContainerDialog,
            None, "test title", db_open(":tutorial:")
        )

    def test_it_sets_default_values_when_opend_without_container(self):
        self.given_editor_without_container()
        self.view.SetName.assert_called_with("")
        self.view.SetCategory.assert_called_with(None)

    def test_it_sets_values_from_opened_container(self):
        self.given_editor_with_container(container_name="my container")
        self.view.SetName.assert_called_with("my container")
        self.view.SetCategory.assert_called_with(None)

    def test_creates_new_container(self):
        self.given_editor_without_container()
        self.view.GetName.return_value = "new container"
        self.controller.on_ok_clicked(None)
        self.assertEqual(self.controller.get_container().get_text(), "new container")

    def test_does_not_save_new_container(self):
        self.given_editor_without_container()
        self.controller.on_ok_clicked(None)
        self.assertEqual(self.db.get_all_events(), [])

    def test_saves_existing_container(self):
        self.view.GetName.return_value = "bar"
        self.given_editor_with_container("foo")
        self.controller.on_ok_clicked(None)
        self.assertEqual([x.text for x in self.db.get_all_events()], ["bar"])

    def test_detects_invalid_names(self):
        self.controller.name = ""
        self.controller.on_ok_clicked(None)
        self.assertTrue(self.view.DisplayInvalidName.called)

    def test_the_dialog_is_not_closed_when_an_invalid_name_is_entered(self):
        self.controller.on_ok_clicked(None)
        self.assertFalse(self.view.EndModalOk.called)

    def given_editor_without_container(self):
        self.controller.on_init(self.db, None)

    def given_editor_with_container(self, container_name):
        start = human_time_to_gregorian("3 Jan 2000 10:01")
        end = human_time_to_gregorian("3 Jan 2000 10:01")
        container = self.db.new_container().update(start, end, container_name)
        self.controller.on_init(self.db, container)

    def setUp(self):
        self.view = Mock(EditContainerDialog)
        self.view.GetName.return_value = ""
        self.view.GetCategory.return_value = None
        self.controller = EditContainerDialogController(self.view)
        self.db = MemoryDB()
