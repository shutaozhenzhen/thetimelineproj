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

from timelinelib.wxgui.utils import BORDER
from timelinelib.editors.fieldselection import FieldSelectionDialogController


class FieldSelectionDialogControllerApi(object):

    def create_field_checkboxes(self, all_fields, fields):
        self.cbxs = []
        for field in all_fields:
            cbx = wx.CheckBox(self, label=field)
            cbx.SetValue(field in fields)
            self.cbxs.append(cbx)
            self.box.Add(cbx, flag=wx.EXPAND | wx.ALL,  border=BORDER)
        self.SetSizerAndFit(self.sizer)

    def get_fields(self):
        fields = []
        for cbx in self.cbxs:
            fields.append((cbx.GetLabel(), cbx.IsChecked()))
        return fields

    def close(self):
        self.EndModal(wx.ID_OK)


class FieldSelectionDialogGuiCreator(wx.Dialog):

    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title, name="field_selection", style=wx.DEFAULT_DIALOG_STYLE)
        self._create_gui()

    def _create_gui(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_input_controls(self.sizer)
        self._create_buttons(self.sizer)
        self._bind()

    def _create_input_controls(self, sizer):
        groupbox = wx.StaticBox(self, wx.ID_ANY, _("Select Fields to Export"))
        self.box = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        sizer.Add(self.box, flag=wx.EXPAND | wx.ALL,  border=BORDER)

    def _create_buttons(self, sizer):
        button_box = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(button_box, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _bind(self):

        def ok_on_click(evt):
            self.controller.on_btn_ok()

        self.Bind(wx.EVT_BUTTON, ok_on_click, id=wx.ID_OK)


class FieldSelectionDialog(FieldSelectionDialogGuiCreator, FieldSelectionDialogControllerApi):

    def __init__(self, parent, title, data, fields):
        FieldSelectionDialogGuiCreator.__init__(self, parent, title=title)
        self.controller = FieldSelectionDialogController(self, data, fields)

    def get_selected_fields(self):
        return self.controller.get_selected_fields()
