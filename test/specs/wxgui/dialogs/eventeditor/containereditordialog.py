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

from timelinelib.data.db import MemoryDB
from timelinelib.data import Container
from timelinelib.wxgui.dialogs.eventeditor.containereditorcontroller import ContainerEditorController
from timelinelib.repositories.interface import EventRepository
from timelinelib.wxgui.dialogs.eventeditor.eventeditordialog import ContainerEditorDialog
from timelinetest import UnitTestCase


class ContainerEditorTestCase(UnitTestCase):

    def setUp(self):
        self.view = Mock(ContainerEditorDialog)
        self.event_repository = Mock(EventRepository)
        self.db = MemoryDB()
        start = self.time("2000-01-03 10:01:01")
        end = self.time("2000-01-03 10:01:01")
        self.container = Container(self.db.get_time_type(), start, end, "Container1")

    def testConstructionWithoutContainer(self):
        self.given_editor_without_container()
        self.view.set_name.assert_called_with("")
        self.view.set_category.assert_called_with(None)

    def testConstructionWithContainer(self):
        self.given_editor_with_container()
        self.view.set_name.assert_called_with("Container1")
        self.view.set_category.assert_called_with(None)

    def testContainerCreated(self):
        self.given_editor_without_container()
        self.editor.save()
        self.view.get_name.assert_called()
        self.view.get_category.assert_called()
        self.assertFalse(self.editor.container is None)

    def given_editor_without_container(self):
        self.editor = ContainerEditorController(self.view, self.db, None)

    def given_editor_with_container(self):
        self.editor = ContainerEditorController(self.view, self.db, self.container)

    def time(self, tm):
        return self.db.get_time_type().parse_time(tm)
