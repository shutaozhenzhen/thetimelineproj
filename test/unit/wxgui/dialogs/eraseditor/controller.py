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


import wx

from unittest.mock import Mock

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from canvas.data.memorydb.db import MemoryDB
from timelinelib.canvas.data.era import Era
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_gregorian_era_with
from timelinelib.wxgui.dialogs.eraeditor.view import EraEditorDialog
from timelinelib.wxgui.dialogs.eraseditor.controller import ErasEditorDialogController
from timelinelib.wxgui.dialogs.eraseditor.view import ErasEditorDialog


class describe_eras_editor_dialog_controller(UnitTestCase):

    def test_construction(self):
        self.assertEqual(2, len(self.controller.eras))
        self.assertEqual(self.view, self.controller.view)

    def test_listbox_is_populated_at_construction(self):
        self.view.SetEras.assert_called_with(self.db.get_all_eras())

    def test_delete_removes_era(self):
        era = self.db.get_all_eras()[0]
        self._simulate_delete_button_clicked_on(era)
        self.view.RemoveEra.assert_called_with(era)
        self.assertEqual(self.db.get_all_eras(), self.controller.eras)

    def test_when_added_the_add_operation_function_is_called(self):
        count = len(self.db.get_all_eras.return_value)
        dlg = Mock(EraEditorDialog)
        dlg.ShowModal.return_value = wx.ID_OK
        self.controller.set_editor_dialog(dlg)
        self.controller.on_add(None)
        self.assertTrue(isinstance(self.view.AppendEra.call_args[0][0], Era))
        self.assertTrue(isinstance(self.db.save_era.call_args[0][0], Era))
        self.assertEqual(count + 1, len(self.db.get_all_eras.return_value))

    def test_when_edited_the_edit_operation_function_is_called(self):
        era = Mock(Era)
        self.view.GetSelectedEra.return_value = era
        dlg = Mock(EraEditorDialog)
        dlg.ShowModal.return_value = wx.ID_OK
        self.controller.set_editor_dialog(dlg)
        self.controller.on_edit(None)
        self.view.UpdateEra.assert_called_with(era)

    def test_doubleclick_acts_as_edit(self):
        era = Mock(Era)
        self.view.GetSelectedEra.return_value = era
        dlg = Mock(EraEditorDialog)
        dlg.ShowModal.return_value = wx.ID_OK
        self.controller.set_editor_dialog(dlg)
        self.controller.on_dclick(None)
        self.view.UpdateEra.assert_called_with(era)

    def _simulate_delete_button_clicked_on(self, era):
        self.view.GetSelectedEra.return_value = era
        self.controller.on_remove(None)

    def setUp(self):
        eras = [a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="Haha"),
                a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="Hey Hey")]
        self.db = Mock(MemoryDB)
        self.db.get_all_eras.return_value = eras
        self.db.time_type = GregorianTimeType()
        self.view = Mock(ErasEditorDialog)
        self.controller = ErasEditorDialogController(self.view)
        self.controller.on_init(self.db, None)
