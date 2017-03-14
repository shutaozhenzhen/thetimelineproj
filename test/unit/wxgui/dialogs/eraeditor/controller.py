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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_gregorian_era_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.dialogs.eraeditor.controller import EraEditorDialogController
from timelinelib.wxgui.dialogs.eraeditor.view import EraEditorDialog


class EraEditorTestCase(UnitTestCase):

    def when_editor_opened_with_era(self, era):
        self.editor = EraEditorDialogController(self.view, era)

    def when_era_has_period(self, start, end):
        self.era = a_gregorian_era_with(start=start, end=end)
        self.controller = EraEditorDialogController(self.view)
        self.controller.on_init(self.era)

    def when_editing_a_new_era(self):
        self.era = a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="")
        self.controller = EraEditorDialogController(self.view, self.era)
        self.view.reset_mock()

    def when_editing_an_era(self):
        self.era = a_gregorian_era_with(start="1 Jan 2010", end="1 Jan 2020", name="Haha")
        self.era_clone = self.era.clone()
        self.controller = EraEditorDialogController(self.view)
        self.view.GetPeriod.return_value = self.era.get_time_period()
        self.simulate_user_enters_name(self.era.get_name())
        self.simulate_user_enters_color(self.era.get_color())
        self.controller.on_init(self.era)

    def assert_era_unchanged(self):
        self.assertEquals(self.era, self.era_clone)

    def simulate_user_enters_period(self, start, end):
        self.view.GetPeriod.return_value = gregorian_period(start, end)

    def simulate_user_enters_name(self, name):
        self.view.GetName.return_value = name

    def simulate_user_enters_color(self, color):
        self.view.GetColor.return_value = color

    def simulate_user_clicks_ok(self):
        self.controller.on_ok(None)

    def setUp(self):
        self.view = Mock(EraEditorDialog)


class describe_era_editor_dialog__period_field(EraEditorTestCase):

    def test_has_value_from_era(self):
        self.when_era_has_period("1 Jan 2010", "1 Jan 2020")
        self.view.SetPeriod.assert_called_with(
            gregorian_period("1 Jan 2010", "1 Jan 2020")
        )


class describe_era_editor_dialog__name_field(EraEditorTestCase):

    def test_has_value_from_era(self):
        self.when_editing_an_era()
        self.view.SetName.assert_called_with(self.era.get_name())


class describe_era_editor__saving(EraEditorTestCase):

    def test_saves_period(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(
            self.era.get_time_period(),
            gregorian_period("1 Jan 2010", "1 Jan 2020")
        )

    def test_saves_name(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_name(), "New event")

    def test_saves_color(self):
        self.when_editing_an_era()
        self.given_saving_valid_era()
        self.assertEqual(self.era.get_color(), (220, 220, 220))

    def given_saving_valid_era(self):
        self.simulate_user_enters_period("1 Jan 2010", "1 Jan 2020")
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

    def test_period_must_be_valid(self):
        self.when_editing_an_era()
        self.view.GetPeriod.side_effect = ValueError
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidPeriod.called)
        self.assert_era_unchanged()

    def test_period_can_be_long(self):
        self.when_editing_an_era()
        self.simulate_user_enters_period("1 Jan 2000", "1 Jan 5000")
        self.simulate_user_clicks_ok()
        self.assertEqual(0, self.view.DisplayInvalidPeriod.call_count)
