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


import sys
import os

import wx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.config.arguments import ApplicationArguments


STDERR = 'stderr.txt'


class Getter():
    def GetUserConfigDir(self):
        return 'FooBar'


class SP():
    def Get(self):
        return Getter()


class describe_application_arguments(UnitTestCase):

    def test_app_has_default_config_path(self):
        """ """
        try:
            sp = wx.StandardPaths
            wx.StandardPaths = SP()
            self.args.parse_from([])
            self.assertEqual(os.path.join('FooBar', '.thetimelineproj.cfg'), self.args.get_config_file_path())
        finally:
            wx.StandardPaths = sp

    def test_can_return_path_to_cofig_file_(self):
        """ """
        self.args.parse_from(['-c', 'c:\\AppData\\.thetimelineproj.cfg'])
        self.assertEqual('c:\\AppData\\.thetimelineproj.cfg', self.args.get_config_file_path())

    def test_debug_is_not_on_by_default(self):
        """ """
        self.args.parse_from([])
        self.assertFalse(self.args.get_debug_flag())

    def test_debug_can_be_turned_on(self):
        """ """
        self.args.parse_from(['--debug'])
        self.assertTrue(self.args.get_debug_flag())

    def test_timeline_file_dont_have_to_be_pecified_at_start(self):
        """ """
        self.args.parse_from([])
        self.assertFalse(self.args.has_files())
        self.assertEqual([], self.args.get_files())
        self.assertTrue(self.args.get_first_file() is None)

    def test_timeline_file_can_be_specified_at_start(self):
        """ """
        FILE = 'test.timeline'
        self.args.parse_from([FILE, "FooBar"])
        self.assertEqual(FILE, self.args.get_first_file())

    def test_multiple_timeline_files_can_be_specified_at_start(self):
        """ """
        FILE1 = 'test.timeline'
        FILE2 = 'FooBar'
        self.args.parse_from([FILE1, FILE2])
        self.assertEqual([FILE1, FILE2], self.args.get_files())

    def test_invalid_option_causes_system_exit(self):
        """ """
        try:
            self.addCleanup(self.remove_stderr_file)
            e = sys.exit
            s = sys.stderr
            sys.exit = self.my_exit
            sys.stderr = open(STDERR, 'w')
            self.args.parse_from(['--invalid'])
            self.assertEqual(2, self.status)
        finally:
            sys.exit = e
            sys.stderr = s

    def my_exit(self, status):
        self.status = status

    def setUp(self):
        self.args = ApplicationArguments()

    def remove_stderr_file(self):
        if os.path.exists(STDERR):
            os.remove(STDERR)
