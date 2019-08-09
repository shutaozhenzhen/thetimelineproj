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
import wx

from timelinelib.wxgui.utils import WildcardHelper
from timelinelib.test.cases.unit import UnitTestCase


class describe_wildcard_helper(UnitTestCase):

    def testGeneratesWildcardStringForUseInFileDialog(self):
        helper = WildcardHelper("Source code files", ["cpp", "py"])
        self.assertEqual(
            helper.wildcard_string(),
            "Source code files (*.cpp, *.py)|*.cpp;*.py")

    def testReturnsExtensionDataIfExtensionDataGivenAndPathMatch(self):
        helper = WildcardHelper("Image files", [("png", 1), ("bmp", 2)])
        self.assertEqual(
            helper.get_extension_data("bar.png"),
            1)

    def testReturnsNoExtensionDataIfPathDoesNotPathExtension(self):
        helper = WildcardHelper("Text files", [("txt", 4)])
        self.assertEqual(
            helper.get_extension_data("bar"),
            None)

    def testReturnsNoExtensionDataIfNoExtensionDataGiven(self):
        helper = WildcardHelper("Text files", ["txt"])
        self.assertEqual(
            helper.get_extension_data("foo.txt"),
            None)

    def testDoesNotAddExtensionIfExtensionAlreadyInPathFromDialog(self):
        helper = WildcardHelper("Image files", ["png", "bmp"])
        self.assertEqual(
            helper.get_path(self.aFileDialogReturningPath("bar.bmp")),
            "bar.bmp")

    def testAddsFirstExtensionIfNoExtensionInPathFromDialog(self):
        helper = WildcardHelper("Image files", ["png", "bmp"])
        self.assertEqual(
            helper.get_path(self.aFileDialogReturningPath("bar")),
            "bar.png")

    def aFileDialogReturningPath(self, path):
        file_dialog = Mock(wx.FileDialog)
        file_dialog.GetPath.return_value = path
        return file_dialog
