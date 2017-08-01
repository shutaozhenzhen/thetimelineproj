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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.frames.mainframe.toolbar import ToolbarCreator
from timelinelib.wxgui.components.timelinepanel import TimelinePanel
from timelinelib.config.dotfile import Config


class describe_toolbar_creator(UnitTestCase):

    def test_has_refernces_to_parent_and_config_when_created(self):
        self.assertTrue(self.toolbar_creator is not None)
        self.assertEqual(self.parent, self.toolbar_creator._parent)
        self.assertEqual(self.config, self.toolbar_creator._config)

    def test_can_create_toolbar(self):
        toolbar = self.toolbar_creator.create()
        self.assertEqual(toolbar, self.toolbar)

    def test_toolbar_can_be_visible(self):
        self.config.show_toolbar = True
        self.toolbar_creator.create()
        self.toolbar.Show.assert_called_once_with(True)

    def test_toolbar_can_be_hidden(self):
        self.config.show_toolbar = False
        self.toolbar_creator.create()
        self.toolbar.Show.assert_called_once_with(False)

    def setUp(self):
        self.parent = Mock(TimelinePanel)
        self.config = Mock(Config)
        self._fake_toolbar_creation()
        self.toolbar_creator = ToolbarCreator(self.parent, self.config)

    def _fake_toolbar_creation(self):
        self.toolbar = Mock()
        self.parent.CreateToolbar.return_value = self.toolbar
