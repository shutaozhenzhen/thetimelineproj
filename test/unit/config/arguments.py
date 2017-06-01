# -*- coding: utf-8 -*-
#
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


import wx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.config.arguments import ApplicationArguments


class Getter():
    def GetUserConfigDir(self):
        return 'FooBar'


class SP():
    def Get(self):
        return Getter()


class describe_application_arguments(UnitTestCase):

    def test_app_has_default_config_path(self):
        sp = wx.StandardPaths
        wx.StandardPaths = SP()
        self.args.parse_from([])
        self.assertEquals('FooBar\\.thetimelineproj.cfg', self.args.get_config_file_path())
        wx.StandardPaths = sp

    def test_can_return_path_to_cofig_file_(self):
        self.args.parse_from(['-c', 'c:\\AppData\\.thetimelineproj.cfg'])
        self.assertEquals('c:\\AppData\\.thetimelineproj.cfg', self.args.get_config_file_path())

    def test_debug_is_not_on_by_default(self):
        self.args.parse_from([])
        self.assertFalse(self.args.get_debug_flag())

    def test_debug_can_be_turned_on(self):
        self.args.parse_from(['--debug'])
        self.assertTrue(self.args.get_debug_flag())

    def test_timeline_file_dont_have_to_be_pecified_at_start(self):
        self.args.parse_from([])
        self.assertFalse(self.args.has_files())
        self.assertEquals([], self.args.get_files())

    def test_timeline_file_can_be_specified_at_start(self):
        FILE = 'test.timeline'
        self.args.parse_from([FILE, "FooBar"])
        self.assertEquals(FILE, self.args.get_first_file())

    def test_multiple_timeline_files_can_be_specified_at_start(self):
        FILE1 = 'test.timeline'
        FILE2 = 'FooBar'
        self.args.parse_from([FILE1, FILE2])
        self.assertEquals([FILE1, FILE2], self.args.get_files())

    def setUp(self):
        self.args = ApplicationArguments()
