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

from timelinelib.wxgui.utils import BORDER
from timelinelib.editors.eras import ErasEditorController


STYLE = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
TITLE = _("Edit Era's")


class ErasEditorDialogGuiCreator(wx.Dialog):
    """
    This class is responsible for the creation of the dialog GUI.
    """

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title=TITLE, name="eras_editor", style=STYLE)
        self._create_gui()

    def _create_gui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_eras_list(sizer)
        self._create_buttons(sizer)
        self.SetSizerAndFit(sizer)
        self._set_size_and_position()
        self._bind()

    def _set_size_and_position(self):
        height = self.GetParent().GetSize()[1] / 2
        self.SetSize((-1, height))
        self.CenterOnParent()

    def _create_eras_list(self, sizer):
        self.eras_list = wx.ListBox(self, wx.ID_ANY)
        sizer.Add(self.eras_list, flag=wx.ALL | wx.EXPAND, border=BORDER, proportion=1)

    def _create_buttons(self, sizer):
        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._create_edit_button(box_sizer)
        self._create_add_button(box_sizer)
        self._create_delete_button(box_sizer)
        box_sizer.AddStretchSpacer()
        self._create_close_button(box_sizer)
        sizer.Add(box_sizer, flag=wx.ALL | wx.EXPAND, border=BORDER)

    def _create_edit_button(self, sizer):
        self.btn_edit = wx.Button(self, wx.ID_EDIT)
        sizer.Add(self.btn_edit, flag=wx.RIGHT, border=BORDER)

    def _create_add_button(self, sizer):
        sizer.Add(wx.Button(self, wx.ID_ADD), flag=wx.RIGHT, border=BORDER)

    def _create_delete_button(self, sizer):
        self.btn_del = wx.Button(self, wx.ID_DELETE)
        sizer.Add(self.btn_del, flag=wx.RIGHT, border=BORDER)
        return self.btn_del

    def _create_close_button(self, sizer):
        sizer.Add(wx.Button(self, wx.ID_CLOSE), flag=wx.LEFT, border=BORDER)

    def _bind(self):

        def window_on_close(evt):
            self.EndModal(wx.ID_CLOSE)

        def on_size(evt):
            self.Layout()

        def btn_edit_on_click(evt):
            self.controller.edit(self._get_selected_era())

        def btn_add_on_click(evts):
            self.controller.add()

        def btn_del_on_click(evt):
            self.controller.delete(self._get_selected_era())

        def btn_close_on_click(evt):
            self.Close()

        self.Bind(wx.EVT_CLOSE, window_on_close)
        self.Bind(wx.EVT_SIZE, on_size, self)
        self.Bind(wx.EVT_BUTTON, btn_edit_on_click, id=wx.ID_EDIT)
        self.Bind(wx.EVT_BUTTON, btn_add_on_click, id=wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, btn_del_on_click, id=wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, btn_close_on_click, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, btn_edit_on_click, self.eras_list)
        self.SetAffirmativeId(wx.ID_CLOSE)

    def _enable_disable_buttons(self):
        if self.eras_list.GetCount() == 0:
            self.btn_del.Enable(False)
            self.btn_edit.Enable(False)
        else:
            self.btn_del.Enable(True)
            self.btn_edit.Enable(True)

    def _get_selected_era(self):
        return self.eras_list.GetClientData(self.eras_list.GetSelection())


class ErasEditorDialogControllerApi(object):
    """
    This class defines the API used by the dialog controller.
    """

    def populate(self, eras):
        for era in eras:
            self.eras_list.Append(era.get_name(), era)
        if len(eras) > 0:
            self.eras_list.SetSelection(0)
        self._enable_disable_buttons()

    def append(self, era):
        self.eras_list.Append(era.get_name(), era)
        self.eras_list.Select(self.eras_list.GetCount() - 1)
        self._enable_disable_buttons()

    def update(self, era):
        self.eras_list.SetString(self.eras_list.GetSelection(), era.get_name())

    def remove(self, era):
        inx = self.eras_list.GetSelection()
        self.eras_list.Delete(inx)
        if self.eras_list.GetCount() == inx:
            inx -= 1
        if inx >= 0:
            self.eras_list.SetSelection(inx)
        self._enable_disable_buttons()


class ErasEditorDialog(ErasEditorDialogGuiCreator, ErasEditorDialogControllerApi):
    """
    Dialog used to edit Era's of a timeline.

    The edits happen immediately. In other words: when the dialog is closing
    all edits have been applied already.
    """

    def __init__(self, parent, timeline, config):
        ErasEditorDialogGuiCreator.__init__(self, parent)
        self.controller = ErasEditorController(self, timeline, config)
