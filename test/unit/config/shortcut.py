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

from timelinelib.config.dotfile import Config
from timelinelib.config.shortcut import ShortcutController
from timelinelib.test.cases.wxapp import WxAppTestCase
import timelinelib.config.shortcut as sc
import timelinelib.wxgui.frames.mainframe.menus as mid


NEW_FUNCTION = "⟪File⟫->⟪New...⟫"
SIDEBAR_FUNCTION = "⟪View⟫->⟪Sidebar⟫"


class ShortcutControllerSpec(WxAppTestCase):

    def test_get_functions_returns_list(self):
        func_list = self.controller.get_functions()
        self.assertTrue(len(func_list) > 0)
        self.assertEqual(NEW_FUNCTION, func_list[0])

    def test_get_function_returns_function(self):
        function = self.controller.get_function("Ctrl+N")
        self.assertEqual(NEW_FUNCTION, function)

    def test_get_modifier_and_key_returns_ok(self):
        modifier, key = self.controller.get_modifier_and_key(NEW_FUNCTION)
        self.assertEqual("Ctrl", modifier)
        self.assertEqual("N", key)

    def test_valid_shortcuts(self):
        self.assertTrue(self.controller.is_valid("", ""))
        for modifier in sc.NON_EMPTY_MODIFIERS:
            self.assertTrue(self.controller.is_valid(modifier, "N"))

    def test_invalid_shortcuts(self):
        self.assertFalse(self.controller.is_valid("", "N"))
        self.assertFalse(self.controller.is_valid("Ctrl", ""))
        self.assertFalse(self.controller.is_valid("Ctrl+", "N"))
        self.assertFalse(self.controller.is_valid("+", "N"))
        self.assertFalse(self.controller.is_valid("+", ""))

    def test_exists(self):
        self.assertTrue(self.controller.exists("Ctrl+N"))

    def test_dont_exists(self):
        self.assertFalse(self.controller.exists("Ctrl+F3"))

    def test_wxid_exists(self):
        self.assertTrue(self.controller.wxid_exists(mid.ID_NEW))

    def test_is_function_key(self):
        for key in sc.FUNCTION_KEYS:
            self.assertTrue(self.controller.is_function_key(key))

    def test_is_not_function_key(self):
        self.assertFalse(self.controller.is_function_key("N"))

    def test_edit(self):
        self.controller.edit(SIDEBAR_FUNCTION, "Ctrl+X")
        function = self.controller.get_function("Ctrl+X")
        self.assertEqual(SIDEBAR_FUNCTION, function)

    def setUp(self):
        WxAppTestCase.setUp(self)
        config = Mock(Config)
        menuitem = wx.MenuItem(wx.Menu("title"), -1, "label")
        self.controller = ShortcutController(config, {mid.ID_SIDEBAR: menuitem, })
