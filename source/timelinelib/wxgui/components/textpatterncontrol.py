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


import humblewx
import wx


class TextPatternControl(wx.TextCtrl):

    def __init__(self, parent, name=None):
        wx.TextCtrl.__init__(self, parent)
        self.controller = TextPatternControlController(self)
        self._bind_events()
        self.controller.on_init()

    def GetValues(self):
        return self.controller.get_values()

    def GetSelectedGroup(self):
        return self.controller.get_selected_group()

    def SetSeparators(self, separators):
        self.controller.set_separators(separators)

    def SetValues(self, values):
        self.controller.set_values(values)

    def SetValuesValidator(self, values_validator):
        self.controller.set_values_validator(values_validator)

    def SetUpHandler(self, up_handler):
        self.controller.set_up_handler(up_handler)

    def SetDownHandler(self, down_handler):
        self.controller.set_down_handler(down_handler)

    def _bind_events(self):
        self.Bind(wx.EVT_CHAR, self.controller.on_char)
        self.Bind(wx.EVT_TEXT, self.controller.on_text)
        self.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.controller.on_kill_focus)

    def _on_set_focus(self, event):
        wx.CallAfter(self.controller.on_after_set_focus)


class TextPatternControlController(humblewx.Controller):

    def on_init(self):
        self.original_background = self.view.GetBackgroundColour()
        self.separators = []
        self.last_selected_group = None
        self.values_validator = None
        self.up_handler = None
        self.down_handler = None

    def on_after_set_focus(self):
        if self.view.GetSelection() != (0, len(self.view.GetValue())):
            return
        elif self.last_selected_group is None:
            self._select_group(self.get_selected_group())
        else:
            self._select_group(self.last_selected_group)

    def on_kill_focus(self, event):
        self.last_selected_group = self.get_selected_group()
        self.view.SetSelection(0, 0)

    def on_text(self, event):
        self._validate()

    def on_char(self, event):
        skip = True
        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ShiftDown():
                skip = self.on_shift_tab()
            else:
                skip = self.on_tab()
        elif (event.GetKeyCode() == wx.WXK_UP and
              self.up_handler is not None and
              self._is_text_valid()):
            self.up_handler(self.view)
            skip = False
        elif (event.GetKeyCode() == wx.WXK_DOWN and
              self.down_handler is not None and
              self._is_text_valid()):
            self.down_handler(self.view)
            skip = False
        event.Skip(skip)

    def on_tab(self):
        return not self._select_group(self.get_selected_group() + 1)

    def on_shift_tab(self):
        return not self._select_group(self.get_selected_group() - 1)

    def get_values(self):
        groups = self._get_groups()
        if groups is None:
            return None
        return [value for (value, start, end) in self._get_groups()]

    def get_selected_group(self):
        (selection_start, _) = self.view.GetSelection()
        for (index, (_, start, end)) in enumerate(self._get_groups()):
            if selection_start >= start and selection_start <= end:
                return index
        return 0

    def set_separators(self, separators):
        self.separators = separators
        self._validate()

    def set_values(self, values):
        (start, end) = self.view.GetSelection()
        text = ""
        for (index, value) in enumerate(values):
            if index > 0:
                text += self.separators[index-1]
            text += value
        self.view.SetValue(text)
        self._validate()
        self.view.SetSelection(start, end)

    def set_values_validator(self, values_validator):
        self.values_validator = values_validator
        self._validate()

    def set_up_handler(self, up_handler):
        self.up_handler = up_handler

    def set_down_handler(self, down_handler):
        self.down_handler = down_handler

    def _get_groups(self):
        text = self.view.GetValue()
        groups = []
        start = 0
        for separator in self.separators:
            separator_pos = text[start:].find(separator)
            if separator_pos == -1:
                return None
            groups.append(self._extract_section(start, start+separator_pos))
            start += separator_pos + len(separator)
        groups.append(self._extract_section(start, len(text)))
        return groups

    def _extract_section(self, start, end):
        return (self.view.GetValue()[start:end], start, end)

    def _validate(self):
        if self._is_text_valid():
            self.view.SetBackgroundColour(self.original_background)
        else:
            self.view.SetBackgroundColour("pink")

    def _is_text_valid(self):
        values = self.get_values()
        if values is None:
            return False
        return self._is_values_valid(values)

    def _is_values_valid(self, values):
        if self.values_validator is None:
            return True
        else:
            return self.values_validator(self.view)

    def _select_group(self, section_to_focus):
        for (index, (_, start, end)) in enumerate(self._get_groups()):
            if index == section_to_focus:
                self.view.SetSelection(start, end)
                return True
        return False
