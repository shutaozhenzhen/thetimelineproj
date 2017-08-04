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
from mock import sentinel

from timelinelib.wxgui.dialogs.export.controller import ExportDialogController
from timelinelib.wxgui.dialogs.export.controller import TARGET_TYPES
from timelinelib.wxgui.dialogs.export.view import ExportDialog
from timelinelib.wxgui.dialogs.fieldselection.controller import FIELDS
from timelinelib.test.cases.unit import UnitTestCase


class describe_export_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(ExportDialog)
        self.controller = ExportDialogController(self.view)
        self.view.GetExportEvents.return_value = False
        self.view.GetExportCategories.return_value = False

    def when_event_type_selected(self):
        self.view.GetExportEvents.return_value = True

    def when_category_type_selected(self):
        self.view.GetExportCategories.return_value = True

    def when_event_fields_selected(self, fields):
        self.controller.event_fields = fields

    def when_category_fields_selected(self, fields):
        self.controller.category_fields = fields

    def simulate_ok_button_clicked(self):
        self.controller.on_ok(None)

    def simulate_edit_event_button_clicked(self):
        self.controller.on_edit_event_fields(None)

    def simulate_edit_category_button_clicked(self):
        self.controller.on_edit_categories_fields(None)

    def test_controller_populates_dialog_when_constructed(self):
        self.controller.on_init()
        self.view.SetTargetTypes.assert_called_with(TARGET_TYPES)
        self.view.SetEvents.assert_called_with(True)
        self.view.SetCategories.assert_called_with(False)
        self.assertEqual(FIELDS["Event"], self.controller.get_event_fields())
        self.assertEqual(FIELDS["Category"], self.controller.get_category_fields())

    def test_no_item_types_selected_generates_info_message(self):
        self.controller.on_ok(None)
        self.view.DisplayInformationMessage.assert_called()

    def test_no_event_fields_selected_generates_info_message(self):
        self.when_event_type_selected()
        self.when_event_fields_selected([])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.DisplayInformationMessage.called)

    def test_no_category_fields_selected_generates_info_message(self):
        self.when_category_type_selected()
        self.when_category_fields_selected([])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.DisplayInformationMessage.called)

    def test_dialog_closes_when_ok_button_is_clicked(self):
        self.when_category_type_selected()
        self.when_category_fields_selected(["Name"])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.Close.called)

    def test_on_edit_event_fields_triggers_view(self):
        self.simulate_edit_event_button_clicked()
        self.assertEqual(self.view.EditEventFields.call_count, 1)

    def test_on_edit_category_fields_triggers_view(self):
        self.simulate_edit_category_button_clicked()
        self.assertEqual(self.view.EditCategoryFields.call_count, 1)

    def test_event_fields_can_be_set(self):
        self.controller.set_event_fields(sentinel.FIELDS)
        self.assertEqual(self.controller.get_event_fields(), sentinel.FIELDS)

    def test_category_fields_can_be_set(self):
        self.controller.set_category_fields(sentinel.FIELDS)
        self.assertEqual(self.controller.get_category_fields(), sentinel.FIELDS)

    def test(self):
        self.view.GetExportEvents.side_effect = ValueError()
        self.when_event_type_selected()
        self.when_event_fields_selected([])
        self.simulate_ok_button_clicked()
        self.assertEqual(self.view.Close.call_count, 0)
