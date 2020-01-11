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


from timelinelib.wxgui.dialogs.eventduration.controller import EventsDurationController
from timelinelib.wxgui.framework import Dialog


class EventDurationDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer
            rows="6"
            columns="2"
            growableColumns="1"
            proportion="1"
            border="ALL">
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(category_text)"
            />
            <CategoryChoice
                name="category_choice"
                allow_add="True"
                timeline="$(db)"
                align="ALIGN_CENTER_VERTICAL"
            />
             <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(duration_type_text)"
            />
            <Choice
                name="duration_type_choice"
                choices="$(duration_type_choices)"
                align="ALIGN_CENTER_VERTICAL"
            />
            <StretchSpacer />
            <StretchSpacer />
            <StretchSpacer />
            <StretchSpacer />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(duration_text)"
            />
            <TextCtrl
                name="txt_duration"
                width="30"
            />
            <StretchSpacer />
            <StretchSpacer />
        </FlexGridSizer>
        <DialogButtonsMeasureCloseSizer
            border="LEFT|BOTTOM|RIGHT"
            event_EVT_BUTTON__ID_OK="on_ok_clicked"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, title, db, category):
        Dialog.__init__(self, EventsDurationController, parent, {
            "db": db,
            "category_text": _("Category:"),
            "duration_text": _("Duration:"),
            "duration_type_text": _("Duration Type:"),
            "duration_type_choices": [_('hours'), _('workdays'), _('days'), _('minutes'), _('seconds')],
        }, title=title)
        self.controller.on_init(db, category)
        self.duration_type_choice.Select(0)

    def PopulateCategories(self, exclude):
        self.category_choice.Populate(exclude=exclude)
        self.Fit()

    def GetCategory(self):
        return self.category_choice.GetSelectedCategory()

    def SetCategory(self, category):
        return self.category_choice.SetSelectedCategory(category)

    def SetDuration(self, duration):
        return self.txt_duration.SetValue(duration)

    def GetDurationType(self):
        inx = self.duration_type_choice.GetSelection()
        return self.duration_type_choice.GetString(inx)


def open_measure_duration_dialog(parent, timeline, config):
    dialog = EventDurationDialog(parent, _('Measure Duration'), timeline, config)
    dialog.ShowModal()
    dialog.Destroy()