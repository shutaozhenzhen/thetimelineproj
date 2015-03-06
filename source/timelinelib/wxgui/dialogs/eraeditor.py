# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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
import wx.lib.colourselect as colourselect

import timelinelib.wxgui.utils as guiutils
from timelinelib.editors.era import EraEditorDialogController
from timelinelib.wxgui.utils import BORDER


class EraEditorDialogGuiCreator(wx.Dialog):
    """
    This class is responsible for the creation of the dialog GUI.
    """

    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title, name="era_editor", style=wx.DEFAULT_DIALOG_STYLE)
        self._create_gui()

    def _create_gui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_properties_controls(sizer)
        self._create_buttons(sizer)
        self.SetSizerAndFit(sizer)
        self._bind()

    def _create_properties_controls(self, sizer):
        groupbox = wx.StaticBox(self, wx.ID_ANY, _("Era Properties"))
        box = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        self._create_details(box)
        sizer.Add(box, flag=wx.EXPAND | wx.ALL, border=BORDER, proportion=1)

    def _create_details(self, sizer):
        grid = wx.FlexGridSizer(4, 2, BORDER, BORDER)
        grid.AddGrowableCol(1)
        self._create_time_details(grid)
        self._create_checkboxes(grid)
        self._create_name_field(grid)
        self._create_color_selector(grid)
        sizer.Add(grid, flag=wx.EXPAND | wx.ALL, border=BORDER, proportion=1)

    def _create_time_details(self, grid):
        grid.Add(wx.StaticText(self, label=_("When:")), flag=wx.ALIGN_CENTER_VERTICAL)
        self.dtp_start = self._create_time_picker("start")
        self.dtp_end = self._create_time_picker()
        when_box = wx.BoxSizer(wx.HORIZONTAL)
        when_box.Add(self.dtp_start, proportion=1)
        when_box.AddSpacer(BORDER)
        when_box.Add(wx.StaticText(self, label=_("to")), flag=wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        when_box.AddSpacer(BORDER)
        when_box.Add(self.dtp_end, proportion=1, flag=wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        grid.Add(when_box)

    def _create_checkboxes(self, grid):
        grid.AddStretchSpacer()
        when_box = wx.BoxSizer(wx.HORIZONTAL)
        if self.time_type.is_date_time_type():
            self.chb_show_time = wx.CheckBox(self, label=_("Show time"))
            when_box.Add(self.chb_show_time)
        grid.Add(when_box)

    def _create_time_picker(self, name=None):
        dtp = guiutils.time_picker_for(self.time_type)(self, config=self.config)
        if name is not None:
            dtp.SetName(name)
        return dtp

    def _create_name_field(self, grid):
        self.txt_name = wx.TextCtrl(self, wx.ID_ANY, name="name")
        grid.Add(wx.StaticText(self, label=_("Name:")), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.txt_name, flag=wx.EXPAND)

    def _create_color_selector(self, grid):
        self.colorpicker = colourselect.ColourSelect(self)
        grid.Add(wx.StaticText(self, label=_("Colour:")), flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.colorpicker)

    def _create_buttons(self, sizer):
        button_box = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(button_box, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _bind(self):

        def ok_on_click(evt):
            self.controller.on_btn_ok()

        def show_time_on_checkbox(evt):
            self.dtp_start.show_time(evt.IsChecked())
            self.dtp_end.show_time(evt.IsChecked())

        self.Bind(wx.EVT_BUTTON, ok_on_click, id=wx.ID_OK)
        if self.time_type.is_date_time_type():
            self.Bind(wx.EVT_CHECKBOX, show_time_on_checkbox, self.chb_show_time)


class EraEditorDialogControllerApi(object):
    """
    This class defines the API used by the dialog controller.
    """

    def close(self):
        self.EndModal(wx.ID_OK)

    def set_focus_on(self, name):
        guiutils.set_focus(self, name)

    def set_start(self, start):
        self.dtp_start.set_value(start)

    def get_start(self):
        return self.dtp_start.get_value()

    def set_name(self, name):
        self.txt_name.SetValue(name)

    def get_name(self):
        return self.txt_name.GetValue().strip()

    def set_end(self, start):
        self.dtp_end.set_value(start)

    def get_end(self):
        return self.dtp_end.get_value()

    def set_color(self, new_color):
        self.colorpicker.SetValue(new_color)

    def get_color(self):
        return self.colorpicker.GetValue()

    def set_show_time(self, checked):
        if self.time_type.is_date_time_type():
            self.chb_show_time.SetValue(checked)
            self.dtp_start.show_time(checked)
            self.dtp_end.show_time(checked)

    def display_invalid_start(self, message):
        self._display_invalid_input(message, self.dtp_start)

    def display_invalid_end(self, message):
        self._display_invalid_input(message, self.dtp_end)

    def display_invalid_name(self, message):
        self._display_invalid_input(message, self.txt_name)

    def display_invalid_color(self, message):
        self._display_invalid_input(message, self.colorpicker)

    def display_invalid_period(self, message):
        guiutils.display_error_message(message, self)

    def _display_invalid_input(self, message, control):
        guiutils.display_error_message(message, self)
        guiutils._set_focus_and_select(control)


class EraEditorDialog(EraEditorDialogGuiCreator, EraEditorDialogControllerApi):

    def __init__(self, parent, title, time_type, config, era):
        self.time_type = time_type
        self.config = config
        EraEditorDialogGuiCreator.__init__(self, parent, title=title)
        self.controller = EraEditorDialogController(self, era, time_type)
