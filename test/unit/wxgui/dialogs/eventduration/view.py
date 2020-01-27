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
from timelinelib.test.cases.wxapp import WxAppTestCase
from timelinelib.wxgui.dialogs.eventduration.view import EventDurationDialog
from timelinelib.db import db_open


class describe_event_duration_dialog(WxAppTestCase):

    def test_show_manual_test_dialog(self):
        """def __init__(self, parent, title, db, config, preferred_category):"""
        db = db_open(":tutorial:")
        config = Mock(Config)
        config.workday_length = 8
        config.get_date_formatter.return_value = GregorianDateFormatter()
        self.show_dialog(
            EventDurationDialog,
            None,
            "Title",
            db,
            config,
            None
        )
