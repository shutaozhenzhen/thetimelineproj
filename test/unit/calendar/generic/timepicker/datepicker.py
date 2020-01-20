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


from unittest.mock import Mock
from unittest.mock import sentinel
import wx

import humblewx

import timelinelib.calendar.generic.timepicker.datepicker as gdp
import timelinelib.calendar.generic.timepicker.datepicker as pdp
from timelinelib.calendar.generic.timepicker.datepickercontroller import DatePickerController
from timelinelib.calendar.generic.timepicker.datepicker import DatePicker
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.framework import Dialog
from timelinelib.calendar.generic.timepicker.datemodifier import DateModifier
from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.calendar.coptic.dateformatter import CopticDateFormatter
from timelinelib.calendar.pharaonic.dateformatter import PharaonicDateFormatter
from timelinelib.calendar.generic.timepicker.datemodifier import DateModifier
from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.pharaonic.pharaonic import PharaonicDateTime
from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.timetype.timetype import PharaonicTimeType


class describe_new_coptic_date_picker(UnitTestCase):

    def test_has_date_formatter(self):
        self.assertEqual(self.controller._date_formatter, self.date_formatter)

    def test_can_set_coptic_date(self):
        self.date_formatter.format.return_value = (
            sentinel.TEXT,
            sentinel.IS_BC,
        )
        self.controller.set_date(sentinel.DATE)
        self.date_formatter.format.assert_called_with(sentinel.DATE)
        self.view.SetText.assert_called_with(sentinel.TEXT)
        self.view.SetIsBc.assert_called_with(sentinel.IS_BC)

    def test_can_get_coptic_date(self):
        self.assertEqual(
            self.controller.get_date(),
            sentinel.PARSED_DATE
        )
        self.date_formatter.parse.assert_called_with((
            sentinel.TEXT,
            sentinel.IS_BC,
        ))

    def test_can_increment_year(self):
        self.set_up_region_type(CopticDateFormatter.YEAR)
        self.controller.on_key_up()
        self.assert_modifier_called(self.date_modifier.increment_year)

    def test_can_increment_month(self):
        self.set_up_region_type(CopticDateFormatter.MONTH)
        self.controller.on_key_up()
        self.assert_modifier_called(self.date_modifier.increment_month)

    def test_can_increment_day(self):
        self.set_up_region_type(CopticDateFormatter.DAY)
        self.controller.on_key_up()
        self.assert_modifier_called(self.date_modifier.increment_day)

    def test_does_not_increment_if_date_is_invalid(self):
        self.date_formatter.parse.side_effect = ValueError
        self.controller.on_key_up()
        self.assertFalse(self.view.SetText.called)

    def test_can_decrement_year(self):
        self.set_up_region_type(CopticDateFormatter.YEAR)
        self.controller.on_key_down()
        self.assert_modifier_called(self.date_modifier.decrement_year)

    def test_can_decrement_month(self):
        self.set_up_region_type(CopticDateFormatter.MONTH)
        self.controller.on_key_down()
        self.assert_modifier_called(self.date_modifier.decrement_month)

    def test_can_decrement_day(self):
        self.set_up_region_type(CopticDateFormatter.DAY)
        self.controller.on_key_down()
        self.assert_modifier_called(self.date_modifier.decrement_day)

    def test_does_not_decrement_if_date_is_invalid(self):
        self.date_formatter.parse.side_effect = ValueError
        self.controller.on_key_down()
        self.assertFalse(self.view.SetText.called)

    def test_sets_error_color_when_date_is_invalid(self):
        self.date_formatter.parse.side_effect = ValueError
        self.controller.on_text(Mock())
        self.view.SetBackgroundColour.assert_called_with("pink")

    def test_sets_ok_color_when_date_invalid(self):
        self.controller.on_text(Mock())
        self.view.SetBackgroundColour.assert_called_with(wx.NullColour)

    def test_tab_moves_to_next_region_if_exists(self):
        self.date_formatter.get_next_region.return_value = sentinel.SELECTION
        self.assertTrue(self.controller.on_tab())
        self.view.SetSelection.assert_called_with(sentinel.SELECTION)
        self.date_formatter.get_next_region.assert_called_with(
            sentinel.TEXT,
            sentinel.CURSOR_POSITION
        )

    def test_tab_returns_false_if_no_next_region(self):
        self.date_formatter.get_next_region.return_value = None
        self.assertFalse(self.controller.on_tab())
        self.assertFalse(self.view.SetSelection.called)
        self.date_formatter.get_next_region.assert_called_with(
            sentinel.TEXT,
            sentinel.CURSOR_POSITION
        )

    def test_shift_tab_moves_to_previous_region_if_exists(self):
        self.date_formatter.get_previous_region.return_value = sentinel.SELECTION
        self.assertTrue(self.controller.on_shift_tab())
        self.view.SetSelection.assert_called_with(sentinel.SELECTION)
        self.date_formatter.get_previous_region.assert_called_with(
            sentinel.TEXT,
            sentinel.CURSOR_POSITION
        )

    def test_shift_tab_returns_false_if_no_next_region(self):
        self.date_formatter.get_previous_region.return_value = None
        self.assertFalse(self.controller.on_shift_tab())
        self.assertFalse(self.view.SetSelection.called)
        self.date_formatter.get_previous_region.assert_called_with(
            sentinel.TEXT,
            sentinel.CURSOR_POSITION
        )

    def set_up_region_type(self, region_type):
        self.date_formatter.get_region_type.return_value = region_type
        self.date_formatter.format.return_value = (
            sentinel.NEW_TEXT,
            sentinel.NEW_IS_BC,
        )

    def setUp(self):
        UnitTestCase.setUp(self)
        self.date_formatter = Mock(CopticDateFormatter)
        self.date_formatter.YEAR = CopticDateFormatter.YEAR
        self.date_formatter.MONTH = CopticDateFormatter.MONTH
        self.date_formatter.DAY = CopticDateFormatter.DAY
        self.date_formatter.parse.return_value = sentinel.PARSED_DATE
        self.date_modifier = Mock()
        modifier_result = sentinel.NEW_DATE
        self.date_modifier.increment_year.return_value = modifier_result
        self.date_modifier.increment_month.return_value = modifier_result
        self.date_modifier.increment_day.return_value = modifier_result
        self.date_modifier.decrement_year.return_value = modifier_result
        self.date_modifier.decrement_month.return_value = modifier_result
        self.date_modifier.decrement_day.return_value = modifier_result
        self.view = Mock(DatePicker)
        self.view.GetText.return_value = sentinel.TEXT
        self.view.GetIsBc.return_value = sentinel.IS_BC
        self.view.GetCursorPosition.return_value = sentinel.CURSOR_POSITION
        self.controller = DatePickerController(self.view)
        self.controller.on_init(self.date_formatter, self.date_modifier)

    def assert_modifier_called(self, modifier):
        self.view.SetText.assert_called_with(sentinel.NEW_TEXT)
        self.view.SetIsBc.assert_called_with(sentinel.NEW_IS_BC)
        modifier.assert_called_with(sentinel.PARSED_DATE)


class describe_new_gregorian_date_picker_view(UnitTestCase):

    def test_show_manual_test_dialog(self):
        try:
            humblewx.COMPONENT_MODULES.insert(0, gdp)
            self.show_dialog(NewGregorianDatePickerTestDialog)
        finally:
            humblewx.COMPONENT_MODULES.remove(gdp)


class NewGregorianDatePickerTestDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="1" border="ALL">
            <Button label="before" />
            <DatePicker
                name="date"
                date_modifier="$(date_modifier)"
                date_formatter="$(date_formatter)"
            />
            <Button label="after" />
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    def __init__(self):
        Dialog.__init__(self, humblewx.Controller, None, {
            "date_modifier": DateModifier(GregorianTimeType(), GregorianDelta, GregorianDateTime),
            "date_formatter": GregorianDateFormatter(),
        })
        self.date.SetDate((2015, 11, 1))


class describe_new_pharaonic_date_picker_view(UnitTestCase):

    def test_show_manual_test_dialog(self):
        try:
            humblewx.COMPONENT_MODULES.insert(0, pdp)
            self.show_dialog(NewPharaonicDatePickerTestDialog)
        finally:
            humblewx.COMPONENT_MODULES.remove(pdp)


class NewPharaonicDatePickerTestDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="1" border="ALL">
            <Button label="before" />
            <DatePicker
                name="date"
                date_modifier="$(date_modifier)"
                date_formatter="$(date_formatter)"
            />
            <Button label="after" />
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    def __init__(self):
        Dialog.__init__(self, humblewx.Controller, None, {
            "date_modifier": DateModifier(PharaonicTimeType(), PharaonicDelta, PharaonicDateTime, max_month=13),
            "date_formatter": PharaonicDateFormatter(),
        })
        self.date.SetDate((2015, 11, 1))

    def _create_date_formatter(self):
        formatter = PharaonicDateFormatter()
        formatter.set_separators("/", " ")
        formatter.set_region_order(year=2, month=1, day=0)
        return formatter
