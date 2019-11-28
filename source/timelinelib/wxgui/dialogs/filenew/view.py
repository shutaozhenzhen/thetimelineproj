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


import wx

from timelinelib.wxgui.dialogs.filenew.controller import FileNewDialogController
from timelinelib.wxgui.framework import Dialog


class FileNewDialog(Dialog):

    """
    <BoxSizerVertical>
        <StaticText
            label="$(explanation_text)"
            border="ALL"
        />
        <BoxSizerHorizontal
            proportion="1"
            border="LEFT|RIGHT"
        >
            <ListBox
                name="type_list"
                width="150"
                height="200"
                event_EVT_LISTBOX="on_selection_changed"
            />
            <StaticBoxSizerVertical
                proportion="1"
                label="$(description_text)"
                border="LEFT"
            >
                <StaticText
                    name="description"
                    width="200"
                    style="ST_NO_AUTORESIZE"
                    proportion="1"
                    border="ALL"
                />
            </StaticBoxSizerVertical>
        </BoxSizerHorizontal>
        <DialogButtonsOkCancelSizer
            border="ALL"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, items):
        Dialog.__init__(self, FileNewDialogController, parent, {
            "explanation_text": _("Choose what type of timeline you want to create."),
            "description_text": _("Description"),
        }, title=_("Create new timeline"), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.controller.on_init(items)

    def SetItems(self, items):
        self.type_list.SetItems(items)
        self.type_list.SetFocus()

    def SelectItem(self, index):
        self.type_list.SetSelection(index)
        event = wx.CommandEvent()
        event.SetInt(index)
        self.controller.on_selection_changed(event)

    def SetDescription(self, text):
        self.description.SetLabel(text)

    def GetSelection(self):
        return self.controller.get_selection()


def open_file_new_dialog(parent):
    items = [
        {
            "text": _("Gregorian"),
            "description": _("This creates a timeline using the standard calendar."),
            "create_fn": parent.create_new_timeline,
        },
        {
            "text": _("Numeric"),
            "description": _("This creates a timeline that has numbers on the x-axis instead of dates."),
            "create_fn": parent.create_new_numeric_timeline,
        },
        {
            "text": _("Directory"),
            "description": _("This creates a timeline where the modification date of files in a directory are shown as events."),
            "create_fn": parent._create_new_dir_timeline,
        },
        {
            "text": _("Bosparanian"),
            "description": _("This creates a timeline using the fictuous Bosparanian calendar from the German pen-and-paper RPG \"The Dark Eye\" (\"Das schwarze Auge\", DSA)."),
            "create_fn": parent.create_new_bosparanian_timeline,
        },
        {
            "text": _("Pharaonic"),
            "description": _("This creates a timeline using the ancient egypt pharaonic calendar"),
            "create_fn": parent.create_new_pharaonic_timeline,
        },
        {
            "text": _("Coptic"),
            "description": _("This creates a timeline using the coptic calendar"),
            "create_fn": parent.create_new_coptic_timeline,
        },
    ]
    dialog = FileNewDialog(parent, items)
    if dialog.ShowModal() == wx.ID_OK:
        dialog.GetSelection()["create_fn"]()
    dialog.Destroy()