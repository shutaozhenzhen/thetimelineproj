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
from timelinelib.wxgui.dialogs.eventduration.controller import PRECISION_CHOICES
from timelinelib.wxgui.framework import Dialog


ALL_CATEGORIES = _('All Categories')


class EventDurationDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer
            rows="8"
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
                allow_add="False"
                timeline="$(db)"
                align="ALIGN_CENTER_VERTICAL"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(duration_type_text)"
            />
            <Choice
                name="duration_type_choices"
                choices="$(duration_type_choices)"
                align="ALIGN_CENTER_VERTICAL"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(precision_text)"
            />
            <Choice
                name="precision_choices"
                choices="$(precision_choices)"
                align="ALIGN_CENTER_VERTICAL"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(copy_to_clibboard_text)"
            />
            <CheckBox
                name="cbx_copy"
            />
            <StretchSpacer />
            <StretchSpacer />
            <StretchSpacer />
            <StretchSpacer />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(duration_text)"
            />
            <StaticText
                name="duration_result"
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

    def __init__(self, parent, title, db, config, preferred_category):
        Dialog.__init__(self, EventsDurationController, parent, {
            "db": db,
            "category_text": _("Category:"),
            "duration_text": _("Duration:"),
            "duration_type_text": _("Duration Type:"),
            "precision_text": _("Nbr of Decimals"),
            "copy_to_clibboard_text": _("Copy to Clipboard"),
            "duration_type_choices": [],
            "precision_choices": PRECISION_CHOICES,
        }, title=title)
        self.controller.on_init(db, config, preferred_category)

    def PopulateCategories(self, exclude):
        self.category_choice.Populate(exclude=exclude)
        self.category_choice.Delete(0)  # Remove blank line
        self.category_choice.Insert(ALL_CATEGORIES, 0)
        self.Fit()

    def GetCategory(self):
        return self.category_choice.GetSelectedCategory()

    def GetPrecision(self):
        return int(self.precision_choices.GetSelection())

    def SelectCategory(self, inx):
        return self.category_choice.Select(inx)

    def SetPreferredCategory(self, preferred_category):
        for inx in range(self.category_choice.GetCount()):
            name = self.category_choice.GetString(inx)
            if name.strip() == preferred_category:
                self.category_choice.SetSelection(inx)
                self.controller.on_ok_clicked(None)
                break

    def SelectPrecision(self, inx):
        return self.precision_choices.Select(inx)

    def SetDuration(self, duration):
        return self.duration_result.SetLabel(duration)

    def SetDurationTypeChoices(self, choices):
        self.duration_type_choices.SetItems(choices)
        self.duration_type_choices.Select(0)

    def SetCopyToClipboard(self, value):
        self.cbx_copy.SetValue(value)

    def GetCopyToClipboard(self):
        return self.cbx_copy.GetValue()

    def GetDurationType(self):
        inx = self.duration_type_choices.GetSelection()
        return self.duration_type_choices.GetString(inx)

    def GetDurationResult(self):
        return self.duration_result.GetLabel()


def open_measure_duration_dialog(parent, timeline, config, preferred_category=ALL_CATEGORIES):
    dialog = EventDurationDialog(parent, _('Measure Duration'), timeline, config, preferred_category)
    dialog.ShowModal()
    dialog.Destroy()