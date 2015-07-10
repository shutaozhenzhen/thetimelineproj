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


from mock import Mock

from timelinelib.wxgui.dialogs.export.fieldselectioncontroller import FIELDS
from timelinelib.wxgui.dialogs.export.fieldselectioncontroller import FieldSelectionDialogController
from timelinelib.wxgui.dialogs.export.fieldselectiondialog import FieldSelectionDialog
from timelinetest import UnitTestCase


class FieldSelectionEditorTestCase(UnitTestCase):

    def a_controller_with(self, data, fields):
        self.selected_fields = []
        for field in fields:
            self.simulate_select_field(field)
        return FieldSelectionDialogController(self.view, data, fields)

    def simulate_select_field(self, field):
        if field not in self.selected_fields:
            self.selected_fields.append((field, True))
            self.view.get_fields.return_value = self.selected_fields

    def simulate_ok_clicked(self):
        self.controller.on_btn_ok()

    def setUp(self):
        self.selected_fields = []
        self.view = Mock(FieldSelectionDialog)


class describe_event_field_selection_editor_dialog_controller(FieldSelectionEditorTestCase):

    def test_construction_when_no_fields_selected(self):
        self.controller = self.a_controller_with("Event", [])
        self.view.create_field_checkboxes.assert_called_with(FIELDS[self.controller.data], [])

    def test_construction_when_some_fields_selected(self):
        self.controller = self.a_controller_with("Event", ["Description"])
        self.view.create_field_checkboxes.assert_called_with(FIELDS[self.controller.data], ["Description"])

    def test_view_closes_when_ok_button_clicked(self):
        self.controller = self.a_controller_with("Event", ["Description"])
        self.simulate_ok_clicked()
        self.view.close.assert_called_with()

    def test_selected_fields_are_returned(self):
        self.controller = self.a_controller_with("Event", ["Description"])
        self.simulate_select_field("Text")
        self.assertEqual(["Description", "Text"], self.controller.get_selected_fields())
