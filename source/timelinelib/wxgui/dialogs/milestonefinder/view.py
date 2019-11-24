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

from timelinelib.wxgui.dialogs.milestonefinder.controller import MilestoneFinderDialogController
from timelinelib.wxgui.framework import Dialog


class MilestoneFinderDialog(Dialog):

    """
    <BoxSizerVertical >

        <ListBox
            name="lst_milestones"
            border="LEFT|RIGHT|BOTTOM"
            height="250"
            proportion="1"
            event_EVT_LISTBOX_DCLICK="on_doubble_click"
        />

        <BoxSizerHorizontal>
        <DialogButtonsOkCancelSizer
            border="LEFT|RIGHT|BOTTOM"
            event_EVT_BUTTON__ID_OK="on_ok"
        />
        </BoxSizerHorizontal>

    </BoxSizerVertical>
    """

    def __init__(self, parent, db):
        Dialog.__init__(self, MilestoneFinderDialogController, parent, {
        }, title=_("Milestone Finder"), style=wx.DEFAULT_DIALOG_STYLE)
        self.controller.on_init(db, parent)

    def SetMilestones(self, milestones):
        self.lst_milestones.SetItems(milestones)
        self.lst_milestones.SetSelection(0)

    def GetMilestone(self):
        return self.lst_milestones.GetString(self.lst_milestones.GetSelection())
