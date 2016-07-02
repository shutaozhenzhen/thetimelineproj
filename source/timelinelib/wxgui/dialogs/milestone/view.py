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


from timelinelib.wxgui.framework import Dialog
from timelinelib.wxgui.dialogs.milestone.controller import EditMilestoneDialogController


class EditMilestoneDialog(Dialog):

    """
    <BoxSizerVertical>

        <StaticBoxSizerVertical label="$(groupbox_text)" border="ALL" >

            <FlexGridSizer rows="0" columns="2" border="ALL">

                <StaticText label="$(when_text)" align="ALIGN_LEFT" />
                <TimePicker time_type="$(time_type)" config="$(config)" name="dtp_time" />

                <Spacer />
                <CheckBox align="ALIGN_CENTER_VERTICAL" label="$(show_time_text)" name="cbx_show_time"
                     event_EVT_CHECKBOX="show_time_checkbox_on_checked" />

                <StaticText label="$(description_text)" align="ALIGN_CENTER_VERTICAL" />
                <TextCtrl name="txt_description" />

                <StaticText label="$(colour_text)" align="ALIGN_CENTER_VERTICAL" />
                <ColourSelect name="colorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />

            </FlexGridSizer>

        </StaticBoxSizerVertical>

        <DialogButtonsOkCancelSizer
            border="LEFT|BOTTOM|RIGHT"
            event_EVT_BUTTON__ID_OK="on_ok_clicked"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, title, time_type, config, milestone):
        Dialog.__init__(self, EditMilestoneDialogController, parent, {
            "groupbox_text": _("Milestone Properties"),
            "when_text": _("When:"),
            "time_type": time_type,
            "show_time_text": _("Show time"),
            "description_text": _("Description:"),
            "colour_text": _("Colour:"),
            "config": config,
        }, title=title)
        self.controller.on_init(milestone, time_type)
        self._milestone = milestone

    def GetTime(self):
        return self.dtp_time.get_value()

    def GetDescription(self):
        return self.txt_description.GetValue()

    def GetColour(self):
        return self.colorpicker.GetValue()
