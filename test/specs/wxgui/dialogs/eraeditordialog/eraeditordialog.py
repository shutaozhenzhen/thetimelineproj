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

from timelinelib.wxgui.dialogs.eraeditordialog.eraeditordialog import EraEditorDialog
from timelinelib.wxgui.dialogs.eraeditordialog.eraeditordialogcontroller import EraEditorDialogController
from timelinetest import UnitTestCase
from timelinetest.utils import create_dialog
from timelinelib.data.db import MemoryDB
from timelinetest.utils import a_gregorian_era_with
from timelinetest.utils import human_time_to_gregorian


GREGORIAN_START = "11 Jul 2014 11:22"
GREGORIAN_END = "11 Jul 2015"
NAME = "New Era"
COLOR = (1, 2, 3)


class describe_EraEditorDialog(UnitTestCase):

    def setUp(self):
        self.db = MemoryDB()
        self.view = Mock(EraEditorDialog)
        self.controller = EraEditorDialogController(self.view)
        self.era = a_gregorian_era_with(name=NAME, color=COLOR, start=GREGORIAN_START, end=GREGORIAN_END)

    def test_it_can_be_created(self):
        with create_dialog(EraEditorDialog, None, "Title", self.db.time_type, None, self.era) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()


class EraEditorTestCase(UnitTestCase):

    def when_editor_opened_with_era(self, era):
        self.editor = EraEditorDialogController(self.view, era)

    def assert_start_time_set_to(self, time):
        self.view.SetStart.assert_called_with(human_time_to_gregorian(time))

    def assert_end_time_set_to(self, time):
        self.view.SetEnd.assert_called_with(human_time_to_gregorian(time))

    def when_era_has_period(self, start, end):
        self.era = a_gregorian_era_with(start=start, end=end)
        self.controller = EraEditorDialogController(self.view)
        self.controller.on_init(self.era, self.era.time_type)

    def when_editing_a_new_era(self):
        self.era = a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="")
        self.controller = EraEditorDialogController(self.view, self.era)
        self.view.reset_mock()

    def when_editing_an_era(self):
        self.era = a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="Haha")
        self.era_clone = self.era.clone()
        self.controller = EraEditorDialogController(self.view)
        self.view.GetStart.return_value = self.era.get_time_period().start_time
        self.view.GetEnd.return_value = self.era.get_time_period().end_time
        self.simulate_user_enters_name(self.era.get_name())
        self.simulate_user_enters_color(self.era.get_color())
        self.controller.on_init(self.era, self.era.time_type)

    def assert_era_unchanged(self):
        self.assertEquals(self.era, self.era_clone)

    def simulate_user_enters_start_time(self, time):
        self.view.GetStart.return_value = human_time_to_gregorian(time)

    def simulate_user_enters_end_time(self, time):
        self.view.GetEnd.return_value = human_time_to_gregorian(time)

    def simulate_user_enters_name(self, name):
        self.view.GetName.return_value = name

    def simulate_user_enters_color(self, color):
        self.view.GetColor.return_value = color

    def simulate_user_clicks_ok(self):
        self.controller.on_ok(None)

    def setUp(self):
        self.view = Mock(EraEditorDialog)
        self.view.GetTimeType.return_value = MemoryDB().time_type


class describe_era_editor_dialog_controller_add(UnitTestCase):

    def setUp(self):
        self.view = Mock(EraEditorDialog)
        self.controller = EraEditorDialogController(self.view)


class describe_era_editor_dialog_controller_edit(UnitTestCase):

    def setUp(self):
        self.view = Mock(EraEditorDialog)
        self.controller = EraEditorDialogController(self.view, self.era)


class describe_era_editor_dialog__start_time_field(EraEditorTestCase):

    def test_has_value_from_era(self):
        self.when_era_has_period("1 Jan 2010", "1 Jan 2020")
        self.assert_start_time_set_to("1 Jan 2010")


class describe_era_editor_dialog__end_time_field(EraEditorTestCase):

    def test_has_value_from_era(self):
        self.when_era_has_period("1 Jan 2010", "1 Jan 2020")
        self.assert_end_time_set_to("1 Jan 2020")


class describe_era_editor_dialog__time_fields(EraEditorTestCase):

    def test_are_shown_if_time_specified(self):
        self.when_era_has_period("1 Jan 2010 15:30", "1 Jan 2020 15:30")
        self.view.SetShowTime.assert_called_with(True)

    def test_are_hidden_if_no_time_specified(self):
        self.when_era_has_period("1 Jan 2010", "1 Jan 2020")
        self.view.SetShowTime.assert_called_with(False)


class describe_era_editor_dialog__name_field(EraEditorTestCase):

    def test_has_value_from_era(self):
        self.when_editing_an_era()
        self.view.SetName.assert_called_with(self.era.get_name())


class describe_era_editor__saving(EraEditorTestCase):

    def test_saves_start_time(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_time_period().start_time, human_time_to_gregorian("1 Jan 2010"))

    def test_saves_end_time(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_time_period().end_time, human_time_to_gregorian("1 Jan 2020"))

    def test_saves_name(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_name(), "New event")

    def test_saves_color(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_color(), (220, 220, 220))

    def given_saving_valid_era(self):
        self.simulate_user_enters_start_time("1 Jan 2010")
        self.simulate_user_enters_end_time("1 Jan 2020")
        self.simulate_user_enters_name("New event")
        self.simulate_user_enters_color((220, 220, 220))
        self.simulate_user_clicks_ok()


class describe_era_editor__validation(EraEditorTestCase):

    def test_name_field_must_not_be_empty(self):
        self.when_editing_an_era()
        self.simulate_user_enters_name("")
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidName.called)
        self.assert_era_unchanged()

    def test_start_must_be_valid(self):
        self.when_editing_an_era()
        self.view.GetStart.return_value = None
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidStart.called)
        self.assert_era_unchanged()

    def test_end_must_be_valid(self):
        self.when_editing_an_era()
        self.view.GetEnd.return_value = None
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidEnd.called)
        self.assert_era_unchanged()

    def test_start_must_be_less_then_end(self):
        self.when_editing_an_era()
        self.simulate_user_enters_start_time("2 Jan 2011")
        self.simulate_user_enters_end_time("1 Jan 2011")
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidStart.called)
        self.assert_era_unchanged()

    def test_period_can_be_long(self):
        self.when_editing_an_era()
        self.simulate_user_enters_start_time("1 Jan 2000")
        self.simulate_user_enters_end_time("1 Jan 5000")
        self.simulate_user_clicks_ok()
        self.assertEqual(0, self.view.DisplayInvalidPeriod.call_count)
