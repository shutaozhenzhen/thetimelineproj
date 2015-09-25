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


import os

import wx

from timelinelib.wxgui.dialogs.eventeditortabselectiondialog.eventeditortabselectiondialogcontroller import EventEditorTabSelectionDialogController
from timelinelib.wxgui.framework import Dialog
from timelinelib.config.paths import ICONS_DIR


class EventEditorTabSelectionDialog(Dialog):

    """
    <BoxSizerVertical>
        <StaticText label="$(header_text)" border="ALL"/>
        <BoxSizerHorizontal proportion="1" >
            <ListBox width="120" height="150" border="LEFT|BOTTOM" proportion="1" />
            <BoxSizerVertical>
                <BitmapButton bitmap="$(up_bitmap)" border="LEFT|RIGHT" />
                <Spacer />
                <BitmapButton bitmap="$(down_bitmap)"  border="LEFT|RIGHT" />
            </BoxSizerVertical>
        </BoxSizerHorizontal>
        <DialogButtonsOkCancelSizer border="RIGHT|BOTTOM" />
    </BoxSizerVertical>
    """

    def __init__(self, parent):
        Dialog.__init__(self, EventEditorTabSelectionDialogController, parent, {
            "header_text": _("Select Tab Order:"),
            "up_bitmap": self._GetBitmap(wx.ART_GO_UP),
            "down_bitmap": self._GetBitmap(wx.ART_GO_DOWN)
        }, title=_("Event Editor Tab Order"),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.controller.on_init()

    def _GetBitmap(self, bitmap_id):
        if 'wxMSW' in wx.PlatformInfo:
            name = {wx.ART_GO_UP: "up.png", wx.ART_GO_DOWN: "down.png"}
            return wx.Bitmap(os.path.join(ICONS_DIR, name[bitmap_id]))
        else:
            size = (24, 24)
            return wx.ArtProvider.GetBitmap(bitmap_id, wx.ART_TOOLBAR, size)
