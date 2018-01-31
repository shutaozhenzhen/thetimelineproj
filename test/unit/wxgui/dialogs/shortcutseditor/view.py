# -*- coding: utf-8 -*-
#
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


from timelinelib.config.shortcut import FUNCTION_KEYS
from timelinelib.config.shortcut import MODIFIERS
from timelinelib.config.shortcut import SHORTCUT_KEYS
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.shortcutseditor.view import ShortcutsEditorDialog


class ShortcutConfig(object):

    def __init__(self):
        self.functions = [u'File->New...', u'File->Save As...']
        self.shc_and_keys = {u'File->New...': ('Ctrl', 'N'),
                             u'File->Save As...': ('Ctrl', 'S')}

    def get_functions(self):
        return self.functions

    def get_modifier_and_key(self, function):
        return self.shc_and_keys[function]

    def get_modifiers(self):
        return MODIFIERS

    def get_shortcuts(self):
        return SHORTCUT_KEYS

    def get_function(self, shortcut):
        for key in self.shc_and_keys:
            if self.shc_and_keys[key][0] + "+" + self.shc_and_keys[key][1] == shortcut:
                return key
        return None

    def edit(self, function, shortcut):
        self.function = function
        self.shortcut = shortcut

    def exists(self, shortcut):
        for key in self.shc_and_keys:
            if self.shc_and_keys[key][0] + "+" + self.shc_and_keys[key][1] == shortcut:
                return True
        return False

    def is_valid(self, modifier, shortcut_key):
        if modifier == "":
            return shortcut_key in ["", ] + FUNCTION_KEYS
        else:
            return modifier in MODIFIERS and shortcut_key in SHORTCUT_KEYS[1:]


class describe_shortcuts_editor_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        self.show_dialog(ShortcutsEditorDialog, None, ShortcutConfig())
