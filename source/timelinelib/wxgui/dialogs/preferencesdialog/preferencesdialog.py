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

from timelinelib.features.experimental.experimentalfeatures import ExperimentalFeatures
from timelinelib.wxgui.dialogs.eventeditor.eventeditortabselectiondialog import SelectTabOrderDialog
from timelinelib.wxgui.dialogs.preferencesdialog.preferencesdialogcontroller import PreferencesDialogController
from timelinelib.wxgui.framework import Dialog


class PreferencesDialog(Dialog):

    """
    <BoxSizerVertical>
        <Notebook border="ALL" proportion="1" width="600">
            <Panel notebookLabel="$(general_text)">
                <BoxSizerVertical>
                    <FlexGridSizer columns="1" border="ALL">
                        <CheckBox
                            name="open_recent"
                            event_EVT_CHECKBOX="on_open_recent_change"
                            label="$(open_recent_text)"
                        />
                        <CheckBox
                            name="inertial_scrolling"
                            event_EVT_CHECKBOX="on_inertial_scrolling_changed"
                            label="$(inertial_scrolling_text)"
                        />
                        <CheckBox
                            name="period_point"
                            event_EVT_CHECKBOX="on_period_point_changed"
                            label="$(period_point_text)"
                        />
                        <CheckBox
                            name="center"
                            event_EVT_CHECKBOX="on_center_changed"
                            label="$(center_text)"
                        />
                        <Button
                            event_EVT_BUTTON="on_tab_order_click"
                            label="$(tab_order_text)"
                            align="ALIGN_LEFT"
                        />
                    </FlexGridSizer>
                </BoxSizerVertical>
            </Panel>
            <Panel notebookLabel="$(date_time_text)">
                <BoxSizerVertical>
                    <FlexGridSizer columns="2" border="ALL">
                        <StaticText label="$(week_start_text)" align="ALIGN_CENTER_VERTICAL" />
                        <Choice
                            name="week_start"
                            event_EVT_CHOICE="on_week_start_changed"
                            choices="$(week_start_choices)"
                        />
                    </FlexGridSizer>
                </BoxSizerVertical>
            </Panel>
            <Panel notebookLabel="$(fonts_text)">
                <BoxSizerVertical>
                    <FlexGridSizer columns="2" border="ALL">
                        <StaticText label="$(major_strip_text)" align="ALIGN_CENTER_VERTICAL" />
                        <Button label="$(edit_text)" />
                        <StaticText label="$(minor_strip_text)" align="ALIGN_CENTER_VERTICAL" />
                        <Button label="$(edit_text)" />
                        <StaticText label="$(legends_text)" align="ALIGN_CENTER_VERTICAL" />
                        <Button label="$(edit_text)" />
                    </FlexGridSizer>
                </BoxSizerVertical>
            </Panel>
            <Panel name="experimental_panel" notebookLabel="$(experimental_text)">
                <BoxSizerVertical>
                    <FlexGridSizer name="experimental_panel_sizer" columns="1" border="ALL">
                    </FlexGridSizer>
                </BoxSizerVertical>
            </Panel>
        </Notebook>
        <DialogButtonsCloseSizer border="LEFT|BOTTOM|RIGHT" />
    </BoxSizerVertical>
    """

    def __init__(self, parent, config):
        Dialog.__init__(self, PreferencesDialogController, parent, {
            "general_text": _("General"),
            "open_recent_text": _("Open most recent timeline on startup"),
            "inertial_scrolling_text": _("Use inertial scrolling"),
            "period_point_text": _("Never show period Events as point Events"),
            "center_text": _("Center Event texts"),
            "tab_order_text": _("Select Event Editor Tab Order"),
            "date_time_text": _("Date && Time"),
            "week_start_text": _("Week start on:"),
            "week_start_choices": [_("Monday"), _("Sunday")],
            "fonts_text": _("Fonts"),
            "major_strip_text": _("Major Strips:"),
            "minor_strip_text": _("Minor Strips:"),
            "legends_text": _("Legends:"),
            "edit_text": _("Edit"),
            "experimental_text": _("Experimental Features"),
        }, title=_("Preferences"))
        self.controller.on_init(config, ExperimentalFeatures())

    def SetCheckboxOpenRecent(self, value):
        self.open_recent.SetValue(value)

    def SetCheckboxInertialScrolling(self, value):
        self.inertial_scrolling.SetValue(value)

    def SetCheckboxPeriodPoint(self, value):
        self.period_point.SetValue(value)

    def SetCheckboxCenterText(self, value):
        self.center.SetValue(value)

    def SetWeekStart(self, value):
        self.week_start.Select(value)

    def AddExperimentalFeatures(self, features):
        for feature in features:
            name = feature.get_display_name()
            cb = wx.CheckBox(self.experimental_panel, label=name)
            cb.SetValue(feature.enabled())
            self.experimental_panel_sizer.Add(cb)
            self.Bind(wx.EVT_CHECKBOX, self.controller.on_experimental_changed, cb)
        self.Fit()

    def ShowSelectTabOrderDialog(self, config):
        dialog = SelectTabOrderDialog(self, config)
        dialog.ShowModal()
        dialog.Destroy()
