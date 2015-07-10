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

from timelinelib.wxgui.dialogs.export.exportcontroller import ExportDialogController
from timelinelib.wxgui.dialogs.export.exportcontroller import TARGET_TYPES
from timelinelib.wxgui.dialogs.export.fieldselection import FIELDS
from timelinelib.wxgui.dialogs.export.exportdialog import ExportDialog
from timelinetest import UnitTestCase


class ExportEditorTestCase(UnitTestCase):

    def when_event_type_selected(self):
        self.view.get_export_events.return_value = True

    def when_category_type_selected(self):
        self.view.get_export_categories.return_value = True

    def when_event_fields_selected(self, fields):
        self.controller.event_fields = fields

    def when_category_fields_selected(self, fields):
        self.controller.category_fields = fields

    def simulate_ok_button_clicked(self):
        self.controller.on_btn_ok()

    def setUp(self):
        self.view = Mock(ExportDialog)
        self.controller = ExportDialogController(self.view)
        self.view.get_export_events.return_value = False
        self.view.get_export_categories.return_value = False


class describe_export_editor_dialog_controller(ExportEditorTestCase):

    def test_controller_populates_dialog_when_constructed(self):
        self.view.set_target_types.assert_called_with(TARGET_TYPES)
        self.view.set_events.assert_called_with(False)
        self.view.set_categories.assert_called_with(False)
        self.assertEqual(FIELDS["Event"], self.controller.get_event_fields())
        self.assertEqual(FIELDS["Category"], self.controller.get_category_fields())

    def test_no_item_types_selected_generates_info_message(self):
        self.controller.on_btn_ok()
        self.view.display_information_message.assert_called()

    def test_no_event_fields_selected_generates_info_message(self):
        self.when_event_type_selected()
        self.when_event_fields_selected([])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.display_information_message.called)

    def test_no_category_fields_selected_generates_info_message(self):
        self.when_category_type_selected()
        self.when_category_fields_selected([])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.display_information_message.called)

    def test_dialog_closes_when_ok_button_is_clicked(self):
        self.when_category_type_selected()
        self.when_category_fields_selected(["Name"])
        self.simulate_ok_button_clicked()
        self.assertTrue(self.view.close.called)
