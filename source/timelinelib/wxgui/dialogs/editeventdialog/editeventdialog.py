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


from timelinelib.wxgui.dialogs.editeventdialog.editeventdialogcontroller import EditEventDialogController
from timelinelib.wxgui.framework import Dialog

import wx


class EditEventDialog(Dialog):

    """
    <BoxSizerVertical>
        <StaticBoxSizerVertical label="$(properties_label)" border="ALL" proportion="1">
            <FlexGridSizer columns="2" growableColumns="1" border="ALL">
                <StaticText align="ALIGN_CENTER_VERTICAL" label="$(when_label)" />
                <Button />
                <StaticText align="ALIGN_CENTER_VERTICAL" label="" />
                <Button />
                <StaticText align="ALIGN_CENTER_VERTICAL" label="$(text_label)" />
                <Button />
                <StaticText align="ALIGN_CENTER_VERTICAL" label="$(category_label)" />
                <Button />
                <StaticText align="ALIGN_CENTER_VERTICAL" label="$(container_label)" />
                <Button />
            </FlexGridSizer>
            <Notebook name="notebook" style="BK_DEFAULT" border="LEFT|RIGHT|BOTTOM" proportion="1" />
        </StaticBoxSizerVertical>
        <CheckBox label="$(add_more_label)" border="LEFT|RIGHT" />
        <DialogButtonsOkCancelSizer border="ALL" />
    </BoxSizerVertical>
    """

    def __init__(self, parent):
        Dialog.__init__(self, EditEventDialogController, parent, {
            "properties_label": _("Event Properties"),
            "when_label": _("When:"),
            "text_label": _("Text:"),
            "category_label": _("Category:"),
            "container_label": _("Container:"),
            "add_more_label": _("Add more events after this one"),
        }, title=_("New dialog title"), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.controller.on_init()
        self.notebook.AddPage(wx.Button(self.notebook), "haha")
        self.notebook.AddPage(wx.Button(self.notebook), "hoho")
        self.Fit()
        self.SetMinSize(self.GetSize())
