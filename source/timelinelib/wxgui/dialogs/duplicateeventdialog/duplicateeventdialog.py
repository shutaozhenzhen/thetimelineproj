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


from timelinelib.wxgui.dialogs.duplicateeventdialog.duplicateeventdialogcontroller import DuplicateEventDialogController
from timelinelib.wxgui.framework import Dialog


class DuplicateEventDialog(Dialog):

    """
    <BoxSizerVertical>

        <BoxSizerHorizontal border="ALL" >
            <StaticText label="$(nbr_of_duplicates_text)" />
            <Spacer />
            <SpinCtrl width="50" name="sc_nbr_of_duplicates" />
        </BoxSizerHorizontal>

        <RadioBox label="$(period_text)" name="rb_periods" choices="$(period_choices)" border="LEFT|RIGHT|BOTTOM" />

        <BoxSizerHorizontal border="LEFT|RIGHT|BOTTOM" >
            <StaticText label="$(frequency_text)" />
            <Spacer />
            <SpinCtrl width="50" />
        </BoxSizerHorizontal>

        <RadioBox label="$(direction_text)" name="rb_periods" choices="$(period_choices)" border="LEFT|RIGHT|BOTTOM" />

        <DialogButtonsOkCancelSizer border="LEFT|RIGHT|BOTTOM" />

    </BoxSizerVertical>
    """

    def __init__(self, parent, db):
        self.db = db
        move_period_config = db.get_time_type().get_duplicate_functions()
        period_list = [label for (label, fn) in move_period_config]
        Dialog.__init__(self, DuplicateEventDialogController, parent, {
            "nbr_of_duplicates_text": _("Number of duplicates:"),
            "period_text": _("Period"),
            "direction_text": _("Direction"),
            "period_choices": period_list,
            "frequency_text": _("Frequency:"),
            "directions": [_("Forward"), _("Backward"), _("Both")],
        }, title=_("Duplicate Event"))
        self.controller.on_init()
        self.sc_nbr_of_duplicates.SetSelection(-1, -1)
