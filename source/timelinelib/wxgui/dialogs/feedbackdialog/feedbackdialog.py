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

from timelinelib.wxgui.dialogs.feedbackdialog.feedbackdialogcontroller import FeedbackDialogController
from timelinelib.wxgui.framework import Dialog


class FeedbackDialog(Dialog):

    """
    <BoxSizerVertical>
        <StaticText name="info" border="LEFT|TOP|RIGHT" />
        <FlexGridSizer columns="2" growableColumns="1" growableRows="2" proportion="1" border="ALL">
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(to_text)" />
            <TextCtrl style="TE_READONLY" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(subject_text)" />
            <TextCtrl />
            <StaticText align="ALIGN_TOP" label="$(body_text)" />
            <TextCtrl height="200" style="TE_MULTILINE" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(send_with_text)" />
            <BoxSizerHorizontal>
                <Button label="$(default_button_text)" borderType="SMALL" border="RIGHT" />
                <Button label="$(gmail_button_text)" borderType="SMALL" border="RIGHT" />
                <Button label="$(other_button_text)" border="RIGHT" />
                <StretchSpacer />
                <DialogButtonsCloseSizer />
            </BoxSizerHorizontal>
        </FlexGridSizer>
    </BoxSizerVertical>
    """

    def __init__(self, parent):
        Dialog.__init__(self, FeedbackDialogController, parent, {
            "title_text": _("Email Feedback"),
            "to_text": _("To:"),
            "subject_text": _("Subject:"),
            "body_text": _("Body:"),
            "send_with_text": _("Send With:"),
            "default_button_text": _("Default client"),
            "gmail_button_text": _("Gmail"),
            "other_button_text": _("Other"),
        }, title=_("Email Feedback"))
        self.controller.on_init()
