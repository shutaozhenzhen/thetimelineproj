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

from timelinelib.canvas.data.memorydb.db import MemoryDB
from timelinelib.wxgui.dialogs.milestonefinder.controller import MilestoneFinderDialogController
from timelinelib.wxgui.dialogs.milestonefinder.view import MilestoneFinderDialog
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with


MILESTONES = [an_event_with(text="A"), an_event_with(text="B")]


class describe_milestone_finder_dialog_controller(UnitTestCase):

    def setUp(self):
        self.mainframe = Mock(MainFrame)
        self.db = Mock(MemoryDB)
        self.db.all_milestones = MILESTONES
        self.view = Mock(MilestoneFinderDialog)
        self.controller = MilestoneFinderDialogController(self.view)
        self.controller.on_init(self.db, None)

    def test_fills_listbox_with_milestones(self):
        self.controller.on_init(self.db, self.mainframe)
        self.view.SetMilestones.assert_called_with(["A", "B"])
