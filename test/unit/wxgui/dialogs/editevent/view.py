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
from timelinelib.wxgui.dialogs.editevent.view import EditEventDialog


class describe_edit_event_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        config = Mock(Config)
        config.get_date_formatter.return_value = GregorianDateFormatter()
        config.get_date_format.return_value = "yyyy-mm-dd"
        config.event_editor_show_period = True
        config.event_editor_show_time = False
        config.event_editor_tab_order = ["0", "1", "2", "3", "4", ":"]
        config.use_date_default_values = True
        config.default_year = 2020
        config.default_month = 1
        config.default_day = 1
        db = db_open(":tutorial:")
        categories = db.get_categories()
        categories[0].parent = categories[1]
        db.save_category(categories[0])
        self.show_dialog(EditEventDialog, None, config, "title", db)

    def test_it_can_be_created_with_numeric_timeline(self):
        config = Mock(Config)
        config.get_date_format.return_value = "yyyy-mm-dd"
        config.event_editor_show_period = True
        config.event_editor_show_time = False
        config.event_editor_tab_order = ["0", "1", "2", "3", "4", ":"]
        config.use_date_default_values = True
        config.default_year = 2020
        config.default_month = 1
        config.default_day = 1
        db = db_open(":numtutorial:")
        categories = db.get_categories()
        categories[0].parent = categories[1]
        db.save_category(categories[0])
        self.show_dialog(EditEventDialog, None, config, "title", db)
