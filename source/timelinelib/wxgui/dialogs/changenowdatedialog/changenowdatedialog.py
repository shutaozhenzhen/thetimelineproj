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


from timelinelib.wxgui.dialogs.changenowdatedialog.changenowdatedialogcontroller import ChangeNowDateDialogController
from timelinelib.wxgui.framework import Dialog


class ChangeNowDateDialog(Dialog):

    """
    <BoxSizerVertical>
        <CheckBox
            label="$(show_time_text)"
            border="LEFT|TOP|RIGHT"
        />
        <TimePicker
            time_type="$(time_type)"
            config="$(config)"
            border="LEFT|BOTTOM|RIGHT"
        />
        <DialogButtonsCloseSizer
            border="LEFT|BOTTOM|RIGHT"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, config, db, handle_new_time_fn, title):
        Dialog.__init__(self, ChangeNowDateDialogController, parent, {
            "show_time_text": _("Show time"),
            "time_type": db.get_time_type(),
            "config": config,
        }, title=title)
        self.controller.on_init()
