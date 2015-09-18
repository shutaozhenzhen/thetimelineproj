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


from timelinelib.wxgui.dialogs.editcategorydialog.editcategorydialogcontroller import EditCategoryDialogController
from timelinelib.wxgui.framework import Dialog


class EditCategoryDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer rows="6" columns="2" border="ALL">
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(name_text)" />
            <TextCtrl id="txt_name" width="150" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(color_text)" />
            <ColourSelect id="colorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(progress_color_text)" />
            <ColourSelect id="progresscolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(done_color_text)" />
            <ColourSelect id="donecolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(font_color_text)" />
            <ColourSelect id="fontcolorpicker" align="ALIGN_CENTER_VERTICAL" width="60" height="30" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(parent_text)" />
            <Choice id="parentlistbox" align="ALIGN_CENTER_VERTICAL" />
        </FlexGridSizer>
        <StdDialogButtonSizer
            buttons="OK|CANCEL"
            border="BOTTOM"
            event_EVT_BUTTON="on_ok_clicked|ID_OK"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent):
        Dialog.__init__(self, EditCategoryDialogController, parent, {
            "name_text": _("Name:"),
            "color_text": _("Color:"),
            "progress_color_text": _("Progress Color:"),
            "done_color_text": _("Done Color:"),
            "font_color_text": _("Font Color:"),
            "parent_text": _("Parent:"),
        }, title=_("New dialog title"))
        self.controller.on_init()
