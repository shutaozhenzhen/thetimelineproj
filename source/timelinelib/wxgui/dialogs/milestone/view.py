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
from timelinelib.db.utils import safe_locking


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

                <StaticText label="$(description_label)" align="ALIGN_CENTER_VERTICAL" />
                <TextCtrl name="txt_label" />

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

    def __init__(self, parent, title, db, config, milestone):
        Dialog.__init__(self, EditMilestoneDialogController, parent, {
            "groupbox_text": _("Milestone Properties"),
            "when_text": _("When:"),
            "time_type": db.time_type,
            "show_time_text": _("Show time"),
            "description_text": _("Description:"),
            "description_label": _("Label:"),
            "colour_text": _("Colour:"),
            "config": config,
        }, title=title)
        self.controller.on_init(db, milestone)
        self._milestone = milestone

    def SetStartTime(self, start_time):
        self.dtp_time.set_value(start_time)

    def SetColor(self, color):
        self.colorpicker.SetValue(color)
        
    def SetDescription(self, description):
        if description is None:
            self.txt_description.SetValue("")
        else:
            self.txt_description.SetValue(description)

    def GetTime(self):
        return self.dtp_time.get_value()

    def GetDescription(self):
        return self.txt_description.GetValue()

    def GetLabel(self):
        return self.txt_label.GetValue()

    def SetLable(self, label):
        self.txt_label.SetValue(label)

    def GetColour(self):
        return self.colorpicker.GetValue()

    def SetShowTime(self, value):
        try:
            self.cbx_show_time.SetValue(value)
            self.dtp_time.show_time(value)
        except:
            # Not all TimePicker objects has a 'show_time' attribute
            pass


def open_milestone_editor_for(parent, config, db, event=None):

    def create_milestone_editor():
        if event is None:
            label = _("Create Milestone")
        else:
            label = _("Edit Milestone")
        return EditMilestoneDialog(parent, label, db, config, event)

    def edit_function():
        dialog = create_milestone_editor()
        dialog.ShowModal()
        dialog.Destroy()
    safe_locking(parent, edit_function)
