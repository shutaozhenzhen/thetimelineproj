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
from timelinelib.wxgui.dialogs.eventduration.controller import EventsDurationController
from timelinelib.wxgui.dialogs.eventduration.controller import PRECISION_CHOICES
from timelinelib.wxgui.framework import Dialog


class EventDurationDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer
            rows="12"
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
                event_EVT_CHOICE="recalculate"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(period_start_text)"
            />
            <BoxSizerHorizontal>
                <CheckBox
                    name="cbx_use_start_period"
                    event_EVT_CHECKBOX="on_use_start_period"
                />
                <Spacer />
                <TimePicker
                    name="start_time"
                    show_time="False"
                    time_type="$(time_type)"
                    config="$(config)"
                    on_change="$(on_change_time)"
                />
                <StretchSpacer size="100"/>
            </BoxSizerHorizontal>
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(period_end_text)"
            />
            <BoxSizerHorizontal>
                <CheckBox
                    name="cbx_use_end_period"
                    event_EVT_CHECKBOX="on_use_end_period"
                />
                <Spacer />
                <TimePicker
                    name="end_time"
                    time_type="$(time_type)"
                    config="$(config)"
                    show_time="False"
                    on_change="$(on_change_time)"
                />
            </BoxSizerHorizontal>
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(duration_type_text)"
            />
            <Choice
                name="duration_type_choices"
                choices="$(duration_type_choices)"
                align="ALIGN_CENTER_VERTICAL"
                event_EVT_CHOICE="recalculate"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(precision_text)"
            />
            <Choice
                name="precision_choices"
                choices="$(precision_choices)"
                align="ALIGN_CENTER_VERTICAL"
                event_EVT_CHOICE="recalculate"
            />
            <StaticText
                align="ALIGN_CENTER_VERTICAL"
                label="$(copy_to_clippboard_text)"
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
            <BoxSizerHorizontal>
                <StaticText
                    name="duration_result"
                    width="150"
                />
                <Spacer />
                <Spacer />
                <Spacer />
                <BitmapButton
                    name="btn_copy"
                    event_EVT_BUTTON="on_copy"
                />
                <Spacer />
            </BoxSizerHorizontal>
            <StretchSpacer />
            <StretchSpacer />
        </FlexGridSizer>

        <DialogButtonsMeasureCloseSizer
            border="LEFT|BOTTOM|RIGHT"
            event_EVT_BUTTON__ID_OK="on_ok_clicked"
        />

    </BoxSizerVertical>
    """

    ALL_CATEGORIES = _('All Categories')

    def __init__(self, parent, title, db, config, preferred_category):
        Dialog.__init__(self, EventsDurationController, parent, {
            "db": db,
            "category_text": _("Category:"),
            "duration_text": _("Duration:"),
            "duration_type_text": _("Duration Type:"),
            "precision_text": _("Number of Decimals:"),
            "copy_to_clippboard_text": _("Autocopy result to Clipboard:"),
            "period_start_text": _("Start at:"),
            "period_end_text": _("Stop at:"),
            "duration_type_choices": [],
            "precision_choices": PRECISION_CHOICES,
            "time_type": db.get_time_type(),
            "config": config,
            "on_change_time": self._recalculate,
            "result_size": (-1, 50),
        }, title=title, size=(100, -1))
        self._init_controls()
        self.controller.on_init(db, config, preferred_category)

    def PopulateCategories(self, exclude):
        self.category_choice.Populate(exclude=exclude)
        self.category_choice.Delete(0)  # Remove blank line
        self.category_choice.Insert(self.ALL_CATEGORIES, 0, None)
        self.Fit()

    def SelectCategory(self, inx):
        return self.category_choice.Select(inx)

    def SetPreferredCategory(self, preferred_category_name):
        for inx in range(self.category_choice.GetCount()):
            category_name = self.category_choice.GetString(inx).strip()
            if category_name == preferred_category_name:
                self.category_choice.SetSelection(inx)
                break

    def GetCategory(self):
        return self.category_choice.GetSelectedCategory()

    def EnableStartTime(self, value):
        self.start_time.Enable(value)

    def SetStartTime(self, value):
        self.start_time.set_value(value)

    def GetStartTime(self):
        if self.start_time.IsEnabled():
            return self.start_time.get_value()

    def EnableEndTime(self, value):
        self.end_time.Enable(value)

    def SetEndTime(self, value):
        self.end_time.set_value(value)

    def GetEndTime(self):
        if self.end_time.IsEnabled():
            return self.end_time.get_value()

    def SelectPrecision(self, inx):
        return self.precision_choices.Select(inx)

    def GetPrecision(self):
        return int(self.precision_choices.GetSelection())

    def SetDurationTypeChoices(self, choices):
        self.duration_type_choices.SetItems(choices)
        self.duration_type_choices.Select(0)

    def GetDurationType(self):
        inx = self.duration_type_choices.GetSelection()
        return self.duration_type_choices.GetString(inx)

    def SetCopyToClipboard(self, value):
        self.cbx_copy.SetValue(value)

    def GetCopyToClipboard(self):
        return self.cbx_copy.GetValue()

    def SetDurationResult(self, duration):
        return self.duration_result.SetLabel(duration)

    def GetDurationResult(self):
        return self.duration_result.GetLabel()

    def _init_controls(self):
        self.btn_copy.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_MENU))
        self.btn_copy.SetToolTip("Copy to clipboard")
        font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.duration_result.SetFont(font)

    def _recalculate(self, evt=None):
        self.controller.recalculate(evt)


def open_measure_duration_dialog(parent, timeline, config, preferred_category=EventDurationDialog.ALL_CATEGORIES):
    dialog = EventDurationDialog(parent, _('Measure Duration of Events'), timeline, config, preferred_category)
    dialog.ShowModal()
    dialog.Destroy()
