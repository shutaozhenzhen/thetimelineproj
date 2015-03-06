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
import timelinelib.wxgui.utils as gui_utils
from timelinelib.editors.eras import ErasEditorController


STYLE = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
TITLE = _("Edit Era's")


class ErasEditorDialog(wx.Dialog):
    """
    Dialog used to edit Era's of a timeline.

    The edits happen immediately. In other words: when the dialog is closing
    all edits have been applied already.
    """

    def __init__(self, parent, eras, timeline, config):
        wx.Dialog.__init__(self, parent, title=TITLE, name="eras_editor", style=STYLE)
        self.eras = timeline.get_all_eras()
        self.timeline = timeline
        self._create_gui()
        self._bind()
        self.controller = ErasEditorController(self, self.eras, self.timeline, config)
        self._enable_disable_buttons()

    def populate_listbox(self, eras):
        for era in eras:
            self.eras_list.Append(era.get_name(), era)
        if len(eras) > 0:
            self.eras_list.SetSelection(0)

    def append(self, era):
        self.eras_list.Append(era.get_name(), era)
        self.eras_list.Select(self.eras_list.GetCount() - 1)
        self._enable_disable_buttons()

    def update(self, era):
        self.eras_list.SetString(self.eras_list.GetSelection(), era.get_name())

    def _create_gui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_eras_list(sizer)
        self._create_buttons(sizer)
        self.SetSizerAndFit(sizer)
        height = self.GetParent().GetSize()[1] / 2
        self.SetSize((-1, height))
        self.CenterOnParent()

    def _create_eras_list(self, sizer):
        self.eras_list = wx.ListBox(self, wx.ID_ANY)
        sizer.Add(self.eras_list, flag=wx.ALL | wx.EXPAND, border=BORDER, proportion=1)

    def _create_buttons(self, sizer):
        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(self._create_edit_button(), flag=wx.RIGHT, border=BORDER)
        box_sizer.Add(self._create_add_button(), flag=wx.RIGHT, border=BORDER)
        box_sizer.Add(self._create_delete_button(), flag=wx.RIGHT, border=BORDER)
        box_sizer.Add(self._create_close_button(), flag=wx.LEFT, border=BORDER)
        sizer.Add(box_sizer, flag=wx.ALL | wx.EXPAND, border=BORDER)

    def _create_edit_button(self):
        self.btn_edit = wx.Button(self, wx.ID_EDIT)
        return self.btn_edit

    def _create_add_button(self):
        return wx.Button(self, wx.ID_ADD)

    def _create_delete_button(self):
        self.btn_del = wx.Button(self, wx.ID_DELETE)
        return self.btn_del

    def _create_close_button(self):
        return wx.Button(self, wx.ID_CLOSE)

    def _bind(self):
        self.Bind(wx.EVT_CLOSE, self._window_on_close)
        self.Bind(wx.EVT_SIZE, self._on_size, self)
        self.Bind(wx.EVT_BUTTON, self._btn_edit_on_click, id=wx.ID_EDIT)
        self.Bind(wx.EVT_BUTTON, self._btn_add_on_click, id=wx.ID_ADD)
        self.Bind(wx.EVT_BUTTON, self._btn_del_on_click, id=wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self._btn_close_on_click, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self._btn_edit_on_click, self.eras_list)
        self.SetAffirmativeId(wx.ID_CLOSE)

    def _on_size(self, evt):
        self.Layout()

    def _lbx_on_dblclick(self, evt):
        pass

    def _window_on_close(self, e):
        self.EndModal(wx.ID_CLOSE)

    def _btn_close_on_click(self, e):
        self.Close()

    def _enable_buttons(self, enabled):
        self.btn_del.Enable(enabled)
        self.btn_edit.Enable(enabled)

    def _updateButtons(self):
        selected_category = self.cat_tree.get_selected_category() is not None
        self._enable_buttons(selected_category)

    def _btn_edit_on_click(self, e):
        self.controller.edit(self.eras_list.GetClientData(self.eras_list.GetSelection()))

    def _btn_add_on_click(self, e):
        self.controller.add()

    def _btn_del_on_click(self, e):
        inx = self.eras_list.GetSelection()
        if self.controller.delete(self.eras_list.GetClientData(inx)):
            self.eras_list.Delete(inx)
            if self.eras_list.GetCount() == inx:
                inx -= 1
            if inx >= 0:
                self.eras_list.SetSelection(inx)
            self._enable_disable_buttons()

    def db_error_handler(self, e):
        gui_utils.handle_db_error_in_dialog(self, e)

    def _enable_disable_buttons(self):
        if self.eras_list.GetCount() == 0:
            self.btn_del.Enable(False)
            self.btn_edit.Enable(False)
        else:
            self.btn_del.Enable(True)
            self.btn_edit.Enable(True)
