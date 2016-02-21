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


from mock import Mock

from timelinelib.calendar.defaultdateformatter import DefaultDateFormatter
from timelinelib.config.dotfile import Config
from timelinelib.db import db_open
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.changenowdate.controller import ChangeNowDateDialogController
from timelinelib.wxgui.dialogs.changenowdate.view import ChangeNowDateDialog


class describe_change_now_date_dialog(UnitTestCase):

    def setUp(self):
        self.view = Mock(ChangeNowDateDialog)
        self.controller = ChangeNowDateDialogController(self.view)

    def test_it_can_be_created(self):
        config = Mock(Config)
        config.get_date_format.return_value = "yyyy-mm-dd"
        config.get_gregorian_date_formatter.return_value = DefaultDateFormatter()
        db = db_open(":tutorial:")
        handle_new_time_fn = Mock()
        title = "a dialog title"
        self.show_dialog(
            ChangeNowDateDialog, None, config, db, handle_new_time_fn, title)
