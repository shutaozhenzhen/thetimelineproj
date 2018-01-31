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


import wx

from mock import Mock

from timelinelib.wxgui.dialogs.eventeditortabselection.view import EventEditorTabSelectionDialog
from timelinelib.test.cases.unit import UnitTestCase


class describe_event_editor_tab_selection_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        config = Mock()
        config.event_editor_tab_order = "01234:"
        self.show_dialog(EventEditorTabSelectionDialog, None, config)

    def setUp(self):
        self.app = wx.App(False)
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

    def tearDown(self):
        self.app.Destroy()
