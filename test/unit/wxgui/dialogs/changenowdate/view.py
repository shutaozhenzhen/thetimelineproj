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


from unittest.mock import Mock

from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.config.dotfile import Config
from timelinelib.db import db_open
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.changenowdate.view import ChangeNowDateDialog


class describe_change_now_date_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        config = Mock(Config)
        config.get_date_formatter.return_value = GregorianDateFormatter()
        handle_new_time_fn = Mock()
        self.show_dialog(
            ChangeNowDateDialog,
            None,
            config,
            db_open(":tutorial:"),
            handle_new_time_fn,
            "a dialog title"
        )
