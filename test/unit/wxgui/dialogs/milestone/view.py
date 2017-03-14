# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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

from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.milestone import Milestone
from timelinelib.config.dotfile import Config
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.dialogs.milestone.view import EditMilestoneDialog


class describe_milestone_editor_dialog(UnitTestCase):

    def test_layout(self):
        db = Mock(MemoryDB)
        db.time_type = GregorianTimeType()
        db.get_categories.return_value = []
        milestone = Milestone(db,
                              human_time_to_gregorian("11 Jul 2014"),
                              "Milestone:1")
        milestone.set_description("a milestone")
        config = Mock(Config)
        config.get_date_formatter.return_value = GregorianDateFormatter()
        self.show_dialog(
            EditMilestoneDialog,
            None,
            "Milestone",
            db,
            config,
            milestone
        )
