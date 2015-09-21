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

from timelinelib.repositories.dbwrapper import DbWrapperCategoryRepository
from timelinelib.wxgui.dialogs.editcategorydialog.editcategorydialogcontroller import EditCategoryDialogController
from timelinelib.wxgui.framework import Dialog
from timelinelib.wxgui.utils import display_error_message
from timelinelib.wxgui.utils import _set_focus_and_select
import timelinelib.wxgui.utils as gui_utils


class EditCategoryDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer rows="6" columns="2" growableColumns="1" proportion="1" border="ALL">
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(name_text)" />
            <TextCtrl name="txt_name" width="150" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(color_text)" />
            <ColourSelect name="colorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(progress_color_text)" />
            <ColourSelect name="progresscolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(done_color_text)" />
            <ColourSelect name="donecolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(font_color_text)" />
            <ColourSelect name="fontcolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(parent_text)" />
            <Choice name="parentlistbox" align="ALIGN_CENTER_VERTICAL" />
        </FlexGridSizer>
        <DialogButtonsOkCancelSizer
            border="LEFT|BOTTOM|RIGHT"
            event_EVT_BUTTON="on_ok_clicked|ID_OK"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, title, db, category):
        Dialog.__init__(self, EditCategoryDialogController, parent, {
            "name_text": _("Name:"),
            "color_text": _("Color:"),
            "progress_color_text": _("Progress Color:"),
            "done_color_text": _("Done Color:"),
            "font_color_text": _("Font Color:"),
            "parent_text": _("Parent:"),
        }, title=title)
        self.controller.on_init(category, DbWrapperCategoryRepository(db))

    def SetCategoryTree(self, tree):
        def add_tree(tree, indent=""):
            for (root, subtree) in tree:
                self.parentlistbox.Append(indent + root.name, root)
                add_tree(subtree, indent + "    ")
        self.parentlistbox.Clear()
        self.parentlistbox.Append("", None)  # No parent
        add_tree(tree)
        self.SetSizerAndFit(self.GetSizer())

    def GetName(self):
        return self.txt_name.GetValue().strip()

    def SetName(self, new_name):
        self.txt_name.SetValue(new_name)

    def GetColor(self):
        return self.colorpicker.GetValueAsRgbTuple()

    def SetColor(self, new_color):
        self.colorpicker.SetValue(new_color)

    def GetProgressColor(self):
        return self.progresscolorpicker.GetValueAsRgbTuple()

    def SetProgressColor(self, new_color):
        self.progresscolorpicker.SetValue(new_color)

    def GetDoneColor(self):
        return self.donecolorpicker.GetValueAsRgbTuple()

    def SetDoneColor(self, new_color):
        self.donecolorpicker.SetValue(new_color)

    def GetFontColor(self):
        return self.fontcolorpicker.GetValueAsRgbTuple()

    def SetFontColor(self, new_color):
        self.fontcolorpicker.SetValue(new_color)

    def GetParent(self):
        selection = self.parentlistbox.GetSelection()
        if selection == wx.NOT_FOUND:
            return None
        return self.parentlistbox.GetClientData(selection)

    def SetParent(self, parent):
        no_items = self.parentlistbox.GetCount()
        for i in range(0, no_items):
            if self.parentlistbox.GetClientData(i) is parent:
                self.parentlistbox.SetSelection(i)
                return

    def HandleInvalidName(self, name):
        msg = _("Category name '%s' not valid. Must be non-empty.")
        display_error_message(msg % name, self)
        _set_focus_and_select(self.txt_name)

    def HandleUsedName(self, name):
        msg = _("Category name '%s' already in use.")
        display_error_message(msg % name, self)
        _set_focus_and_select(self.txt_name)

    def HandleDbError(self, e):
        gui_utils.handle_db_error_in_dialog(self, e)

    def GetEditedCategory(self):
        return self.controller.get_edited_category()
