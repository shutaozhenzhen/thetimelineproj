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

from timelinelib.wxgui.dialogs.categoryfinderdialog.categoryfinderdialogcontroller import CategoryFinderDialogController
from timelinelib.wxgui.framework import Dialog


class CategoryFinderDialog(Dialog):

    """
    <BoxSizerVertical >
        <TextCtrl border="ALL" width="250" />
        <ListBox  border="LEFT|RIGHT|BOTTOM" height="250" proportion="1" />
        <DialogButtonsCheckUncheckCloseSizer border="LEFT|RIGHT|BOTTOM" />
    </BoxSizerVertical>
    """

    def __init__(self, parent, db):
        Dialog.__init__(self, CategoryFinderDialogController, parent, {
            "test_text": "Hello World",
        }, title=_("Category Finder"), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.controller.on_init(db)
