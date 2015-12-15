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


import wx

from timelinelib.calendar.gregorian import Gregorian, GregorianUtils
from timelinelib.calendar import get_date_formatter
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.time.timeline import delta_from_days


class GregorianDatePicker(wx.TextCtrl):

    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_PROCESS_ENTER)
        self.controller = GregorianDatePickerController(self)
        self._bind_events()
        self._resize_to_fit_text()
        self.parent = parent

    def get_value(self):
        return self.controller.get_value()

    def set_value(self, date):
        self.controller.set_value(date)

    def get_date_string(self):
        return self.GetValue()

    def set_date_string(self, date_string):
        return self.SetValue(date_string)

    def _bind_events(self):
        def on_set_focus(evt):
            # CallAfter is a trick to prevent default behavior of selecting all
            # text when a TextCtrl is given focus
            wx.CallAfter(self.controller.on_set_focus)
        self.Bind(wx.EVT_SET_FOCUS, on_set_focus)
        def on_kill_focus(evt):
            # Trick to not make selection text disappear when focus is lost (we
            # remove the selection instead)
            self.controller.on_kill_focus()
            self.SetSelection(0, 0)
        self.Bind(wx.EVT_KILL_FOCUS, on_kill_focus)
        def on_char(evt):
            if evt.GetKeyCode() == wx.WXK_TAB:
                if evt.ShiftDown():
                    skip = self.controller.on_shift_tab()
                else:
                    skip = self.controller.on_tab()
            else:
                skip = True
            evt.Skip(skip)
        self.Bind(wx.EVT_CHAR, on_char)
        def on_text(evt):
            self.controller.on_text_changed()
        self.Bind(wx.EVT_TEXT, on_text)
        def on_key_down(evt):
            if evt.GetKeyCode() == wx.WXK_UP:
                self.controller.on_up()
            elif evt.GetKeyCode() == wx.WXK_DOWN:
                self.controller.on_down()
            elif (evt.GetKeyCode() == wx.WXK_NUMPAD_ENTER or
                  evt.GetKeyCode() == wx.WXK_RETURN):
                self.parent.on_return()
            elif (evt.GetKeyCode() == wx.WXK_ESCAPE):
                self.parent.on_escape()
            else:
                evt.Skip()
        self.Bind(wx.EVT_KEY_DOWN, on_key_down)

    def _resize_to_fit_text(self):
        w, _ = self.GetTextExtent("0000-00-00")
        width = w + 20
        self.SetMinSize((width, -1))


class GregorianDatePickerController(object):

    def __init__(self, date_picker, error_bg="pink"):
        self.date_picker = date_picker
        self.error_bg = error_bg
        self.original_bg = self.date_picker.GetBackgroundColour()
        self.date_formatter = get_date_formatter()
        self.separator = self.date_formatter.separator()
        self.region_year, self.region_month, self.region_day = self.date_formatter.get_regions()
        self.region_siblings = ((self.region_year, self.region_month),
                                (self.region_month, self.region_day))
        self.preferred_day = None
        self.save_preferred_day = True
        self.last_selection = None

    def get_value(self):
        try:
            (year, month, day) = self._parse_year_month_day()
            self._ensure_within_allowed_period((year, month, day))
            return (year, month, day)
        except ValueError:
            raise ValueError("Invalid date.")

    def set_value(self, value):
        year, month, day = value
        date_string = get_date_formatter().format(year, month, day)
        self.date_picker.set_date_string(date_string)

    def on_set_focus(self):
        if self.last_selection:
            start, end = self.last_selection
            self.date_picker.SetSelection(start, end)
        else:
            self._select_region_if_possible(self.region_year)
            self.last_selection = self.date_picker.GetSelection()

    def on_kill_focus(self):
        if self.last_selection:
            self.last_selection = self.date_picker.GetSelection()

    def on_tab(self):
        for (left_region, right_region) in self.region_siblings:
            if self._insertion_point_in_region(left_region):
                self._select_region_if_possible(right_region)
                return False
        return True

    def on_shift_tab(self):
        for (left_region, right_region) in self.region_siblings:
            if self._insertion_point_in_region(right_region):
                self._select_region_if_possible(left_region)
                return False
        return True

    def on_text_changed(self):
        self._change_background_depending_on_date_validity()
        if self._current_date_is_valid():
            current_date = self.get_value()
            # To prevent saving of preferred day when year or month is changed
            # in on_up() and on_down()...
            # Save preferred day only when text is entered in the date text
            # control and not when up or down keys has been used.
            # When up and down keys are used, the preferred day is saved in
            # on_up() and on_down() only when day is changed.
            if self.save_preferred_day:
                self._save_preferred_day(current_date)

    def on_up(self):
        max_year = GregorianUtils.from_time(GregorianTimeType().get_max_time()[0]).year
        def increment_year(date):
            year, month, day = date
            if year < max_year - 1:
                return self._set_valid_day(year + 1, month, day)
            return date
        def increment_month(date):
            year, month, day = date
            if month < 12:
                return self._set_valid_day(year, month + 1, day)
            elif year < max_year - 1:
                return self._set_valid_day(year + 1, 1, day)
            return date
        def increment_day(date):
            year, month, day = date
            time = GregorianUtils.from_date(year, month, day).to_time()
            if time <  GregorianTimeType().get_max_time()[0] - delta_from_days(1):
                return GregorianUtils.from_time(time + delta_from_days(1)).to_date_tuple()
            return date
        if not self._current_date_is_valid():
            return
        selection = self.date_picker.GetSelection()
        current_date = self.get_value()
        if self._insertion_point_in_region(self.region_year):
            new_date = increment_year(current_date)
        elif self._insertion_point_in_region(self.region_month):
            new_date = increment_month(current_date)
        else:
            new_date = increment_day(current_date)
            self._save_preferred_day(new_date)
        if current_date != new_date:
            self._set_new_date_and_restore_selection(new_date, selection)

    def on_down(self):
        def decrement_year(date):
            year, month, day = date
            if year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
                return self._set_valid_day(year - 1, month, day)
            return date
        def decrement_month(date):
            year, month, day = date
            if month > 1:
                return self._set_valid_day(year, month - 1, day)
            elif year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
                return self._set_valid_day(year - 1, 12, day)
            return date
        def decrement_day(date):
            year, month, day = date
            if day > 1:
                return self._set_valid_day(year, month, day - 1)
            elif month > 1:
                return self._set_valid_day(year, month - 1, 31)
            elif year > GregorianUtils.from_time(GregorianTimeType().get_min_time()[0]).year:
                return self._set_valid_day(year - 1, 12, 31)
            return date
        if not self._current_date_is_valid():
            return
        selection = self.date_picker.GetSelection()
        current_date = self.get_value()
        if self._insertion_point_in_region(self.region_year):
            new_date = decrement_year(current_date)
        elif self._insertion_point_in_region(self.region_month):
            new_date = decrement_month(current_date)
        else:
            year, month, day = current_date
            GregorianUtils.from_date(year, month, day)
            if GregorianUtils.from_date(year, month, day).to_time() == GregorianTimeType().get_min_time()[0]:
                return 
            new_date = decrement_day(current_date)
            self._save_preferred_day(new_date)
        if current_date != new_date:
            self._set_new_date_and_restore_selection(new_date, selection)

    def _change_background_depending_on_date_validity(self):
        if self._current_date_is_valid():
            self.date_picker.SetBackgroundColour(self.original_bg)
        else:
            self.date_picker.SetBackgroundColour(self.error_bg)
        self.date_picker.SetFocus()
        self.date_picker.Refresh()

    def _parse_year_month_day(self):
        return get_date_formatter().parse(self.date_picker.get_date_string())

    def _ensure_within_allowed_period(self, date):
        year, month, day = date
        time = Gregorian(year, month, day, 0, 0, 0).to_time()
        if (time >= GregorianTimeType().get_max_time()[0] or
           time < GregorianTimeType().get_min_time()[0]):
            raise ValueError()

    def _set_new_date_and_restore_selection(self, new_date, selection):
        def restore_selection(selection):
            self.date_picker.SetSelection(selection[0], selection[1])
        self.save_preferred_day = False
        if self.preferred_day is not None:
            year, month, _ = new_date
            new_date = self._set_valid_day(year, month, self.preferred_day)
        self.set_value(new_date)
        restore_selection(selection)
        self.save_preferred_day = True

    def _set_valid_day(self, new_year, new_month, new_day):
        done = False
        while not done:
            try:
                date = GregorianUtils.from_date(new_year, new_month, new_day)
                done = True
            except Exception:
                new_day -= 1
        return date.to_date_tuple()

    def _save_preferred_day(self, date):
        _, _, day = date
        if day > 28:
            self.preferred_day = day
        else:
            self.preferred_day = None

    def _current_date_is_valid(self):
        try:
            self.get_value()
        except ValueError:
            return False
        return True

    def _select_region_if_possible(self, region):
        region_range = self._get_region_range(region)
        if region_range:
            self.date_picker.SetSelection(region_range[0], region_range[-1])

    def _insertion_point_in_region(self, n):
        region_range = self._get_region_range(n)
        if region_range:
            return self.date_picker.GetInsertionPoint() in region_range

    def _get_region_range(self, n):
        # Returns a range of valid cursor positions for a valid region year,
        # month or day.
        def region_is_not_valid(region):
            return region not in (self.region_year, self.region_month,
                                  self.region_day)
        def date_has_exactly_two_seperators(datestring):
            return len(datestring.split(self.separator)) == 3
        def calculate_pos_range(region, datestring):
            pos_of_separator1 = datestring.find(self.separator)
            pos_of_separator2 = datestring.find(self.separator,
                                                pos_of_separator1 + 1)
            if region == self.region_year:
                return range(0, pos_of_separator1 + 1)
            elif region == self.region_month:
                return range(pos_of_separator1 + 1, pos_of_separator2 + 1)
            else:
                return range(pos_of_separator2 + 1, len(datestring) + 1)
        if region_is_not_valid(n):
            return None
        date = self.date_picker.get_date_string()
        if not date_has_exactly_two_seperators(date):
            return None
        pos_range = calculate_pos_range(n, date)
        return pos_range
