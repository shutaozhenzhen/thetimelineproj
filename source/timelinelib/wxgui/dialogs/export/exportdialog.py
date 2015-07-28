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

from timelinelib.wxgui.dialogs.export.exportcontroller import ExportController
from timelinelib.wxgui.utils import BORDER
from timelinelib.wxgui.dialogs.export.fieldselectiondialog import FieldSelectionDialog
from timelinelib.wxgui.utils import display_information_message


class ExportDialogGuiCreator(wx.Dialog):
    """
    This class is responsible for the creation of the dialog GUI.
    """

    def __init__(self, parent, title):
        self.parent = parent
        wx.Dialog.__init__(self, parent, title=title, name="era_editor", style=wx.DEFAULT_DIALOG_STYLE)
        self._create_gui()

    def _create_gui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_input_controls(sizer)
        self._create_buttons(sizer)
        self.SetSizerAndFit(sizer)
        self._bind()

    def _create_input_controls(self, sizer):
        self._create_target_types_group(sizer)
        self._create_text_encoding_group(sizer)
        self._create_selection_group(sizer)

    def _create_target_types_group(self, sizer):
        groupbox = wx.StaticBox(self, wx.ID_ANY, _("Select Export File Type"))
        content = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        self._create_target_types_lb(content)
        sizer.Add(content, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _create_target_types_lb(self, sizer):
        self._lb_target_types = wx.ListBox(self, choices=[], style=wx.LB_SINGLE)
        sizer.Add(self._lb_target_types, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _create_text_encoding_group(self, sizer):
        groupbox = wx.StaticBox(self, wx.ID_ANY, _("Select Text Encoding"))
        content = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        self._create_text_encoding_lb(content)
        sizer.Add(content, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _create_text_encoding_lb(self, sizer):
        self._lb_text_encodings = wx.ListBox(self, choices=[], style=wx.LB_SINGLE)
        sizer.Add(self._lb_text_encodings, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _create_selection_group(self, sizer):
        groupbox = wx.StaticBox(self, wx.ID_ANY, _("Select Items to export"))
        content = wx.StaticBoxSizer(groupbox, wx.VERTICAL)
        self._create_selection_cbxs(content)
        sizer.Add(content, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _create_selection_cbxs(self, sizer):
        funcs = (self._create_events_cbx, self._create_categories_cbx)
        grid = wx.GridSizer(rows=len(funcs), cols=2, hgap=5, vgap=5)
        for func in funcs:
            func(grid)
        sizer.Add(grid)

    def _create_events_cbx(self, sizer):
        self._cbx_events = wx.CheckBox(self, label=_("Events"))
        self._btn_events = wx.Button(self, label=_("Select Fields..."))
        sizer.Add(self._cbx_events, flag=wx.EXPAND | wx.ALL,  border=BORDER)
        sizer.Add(self._btn_events)

    def _create_categories_cbx(self, sizer):
        self._cbx_categories = wx.CheckBox(self, label=_("Categories"))
        self._btn_categories = wx.Button(self, label=_("Select Fields..."))
        sizer.Add(self._cbx_categories, flag=wx.EXPAND | wx.ALL,  border=BORDER)
        sizer.Add(self._btn_categories)

    def _create_buttons(self, sizer):
        button_box = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(button_box, flag=wx.EXPAND | wx.ALL, border=BORDER)

    def _bind(self):

        def ok_on_click(evt):
            self.controller.on_btn_ok()

        def on_select_event_fields_click(evt):
            dlg = FieldSelectionDialog(self.parent, _("Select Event Fields"), _("Event"),
                                       self.controller.get_event_fields())
            if dlg.ShowModal() == wx.ID_OK:
                self.controller.set_event_fields(dlg.get_selected_fields())
            dlg.Destroy()

        def on_select_categories_fields_click(evt):
            dlg = FieldSelectionDialog(self.parent, _("Select Category Fields"), _("Category"),
                                       self.controller.get_category_fields())
            if dlg.ShowModal() == wx.ID_OK:
                self.controller.set_category_fields(dlg.get_selected_fields())
            dlg.Destroy()

        self.Bind(wx.EVT_BUTTON, ok_on_click, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, on_select_event_fields_click, self._btn_events)
        self.Bind(wx.EVT_BUTTON, on_select_categories_fields_click, self._btn_categories)


class ExportDialogControllerApi(object):
    """
    This class defines the API used by the dialog controller and dialog creator.
    """

    def close(self):
        self.EndModal(wx.ID_OK)

    def set_target_types(self, types):
        self._lb_target_types.AppendItems(types)
        self._lb_target_types.Select(0)

    def set_text_encodings(self, encodings):
        self._lb_text_encodings.AppendItems(encodings)
        self._lb_text_encodings.Select(0)

    def set_events(self, state):
        self._cbx_events.SetValue(state)

    def set_categories(self, state):
        self._cbx_categories.SetValue(state)

    def get_export_events(self):
        return self._cbx_events.GetValue()

    def get_export_categories(self):
        return self._cbx_categories.GetValue()

    def get_export_type(self):
        return self._lb_target_types.GetStringSelection()

    def get_text_encoding(self):
        return self._lb_text_encodings.GetStringSelection()

    def get_event_fields(self):
        return self.controller.get_event_fields()

    def get_category_fields(self):
        return self.controller.get_category_fields()

    def display_information_message(self, label, text):
        display_information_message(label, text, self)


class ExportDialog(ExportDialogGuiCreator, ExportDialogControllerApi):

    def __init__(self, parent, title):
        ExportDialogGuiCreator.__init__(self, parent, title=title)
        self.controller = ExportController(self)
