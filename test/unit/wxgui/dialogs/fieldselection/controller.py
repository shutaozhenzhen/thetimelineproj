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

from timelinelib.wxgui.dialogs.fieldselection.controller import FIELDS
from timelinelib.wxgui.dialogs.fieldselection.controller import FieldSelectionDialogController
from timelinelib.wxgui.dialogs.fieldselection.view import FieldSelectionDialog
from timelinelib.test.cases.unit import UnitTestCase


class FieldSelectionDialogControllerTestCase(UnitTestCase):

    def a_controller_with(self, data, fields):
        self.selected_fields = []
        for field in fields:
            self.simulate_select_field(field)
        controller = FieldSelectionDialogController(self.view)
        controller.on_init(data, fields)
        return controller

    def simulate_select_field(self, field):
        if field not in self.selected_fields:
            self.selected_fields.append((field, True))
            self.view.GetFields.return_value = self.selected_fields

    def setUp(self):
        self.selected_fields = []
        self.view = Mock(FieldSelectionDialog)

    def test_construction_when_no_fields_selected(self):
        self.controller = self.a_controller_with("Event", [])
        self.view.CreateFieldCheckboxes.assert_called_with(FIELDS[self.controller.data], [])

    def test_construction_when_some_fields_selected(self):
        self.controller = self.a_controller_with("Event", ["Description"])
        self.view.CreateFieldCheckboxes.assert_called_with(FIELDS[self.controller.data], ["Description"])

    def test_construction_when_data_is_a_translatable_text(self):
        self.controller = self.a_controller_with("#Event#", ["Description"])
        self.view.CreateFieldCheckboxes.assert_called_with(FIELDS[self.controller.data], ["Description"])

    def test_selected_fields_are_returned(self):
        self.controller = self.a_controller_with("Event", ["Description"])
        self.simulate_select_field("Text")
        self.assertEqual(["Description", "Text"], self.controller.get_selected_fields())
