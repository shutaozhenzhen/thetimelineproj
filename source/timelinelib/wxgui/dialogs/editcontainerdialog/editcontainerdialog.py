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


from timelinelib.wxgui.dialogs.editcontainerdialog.editcontainerdialogcontroller import EditContainerDialogController
from timelinelib.wxgui.framework import Dialog


class EditContainerDialog(Dialog):

    """
    <BoxSizerVertical>
        <FlexGridSizer columns="2" growableColumns="1" proportion="1" border="ALL">
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(name_text)" />
            <TextCtrl name="txt_name" width="150" />
            <StaticText align="ALIGN_CENTER_VERTICAL" label="$(category_text)" />
            <CategoryChoice name="category_choice" allow_add="True" timeline="$(db)" align="ALIGN_CENTER_VERTICAL" />
        </FlexGridSizer>
        <DialogButtonsOkCancelSizer
            border="LEFT|BOTTOM|RIGHT"
            event_EVT_BUTTON="on_ok_clicked|ID_OK"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, title, db, container=None):
        Dialog.__init__(self, EditContainerDialogController, parent, {
            "db": db,
            "name_text": _("Name:"),
            "category_text": _("Category:"),
        }, title=title)
        self.controller.on_init()

    def PopulateCategories(self):
        self.category_choice.Populate()
        self.Fit()
