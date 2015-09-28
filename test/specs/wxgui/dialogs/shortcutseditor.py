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

from timelinelib.config.shortcut import FUNCTION_KEYS
from timelinelib.config.shortcut import MODIFIERS
from timelinelib.config.shortcut import SHORTCUT_KEYS
from timelinelib.wxgui.dialogs.shortcutseditor.shortcutseditordialogcontroller import ShortcutsEditorDialogController
from timelinelib.wxgui.dialogs.shortcutseditor.shortcutseditordialog import ShortcutsEditorDialog
from timelinetest import UnitTestCase
from timelinetest.utils import create_dialog


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
            return shortcut_key in ["",] + FUNCTION_KEYS
        else:
            return modifier in MODIFIERS and shortcut_key in SHORTCUT_KEYS[1:]


class describe_ShortcutsEditorDialog(UnitTestCase):

    def setUp(self):
        self.view = Mock(ShortcutsEditorDialog)
        self.shortcut_config = ShortcutConfig()
        self.controller = ShortcutsEditorDialogController(self.view)
        self.controller.shortcut_config = self.shortcut_config

    def test_it_can_be_created(self):
        with create_dialog(ShortcutsEditorDialog, None, self.shortcut_config) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()

    def test_shortcut_is_modifier_plus_key(self):
        self.view.GetModifier.return_value = "Ctrl"
        self.view.GetShortcutKey.return_value = "X"
        self.assertEquals("Ctrl+X", self.controller._get_shortcut())

    def test_shortcut_is_key_only(self):
        self.view.GetModifier.return_value = ""
        self.view.GetShortcutKey.return_value = "X"
        self.assertEquals("X", self.controller._get_shortcut())

    def test_shortcut_is_saved(self):
        self.view.GetFunction.return_value = "Func"
        self.view.GetModifier.return_value = "Ctrl"
        self.view.GetShortcutKey.return_value = "X"
        self.controller.on_apply_clicked(None)
        self.assertEquals("Func", self.shortcut_config.function)
        self.assertEquals("Ctrl+X", self.shortcut_config.shortcut)

    def test_shortcut_cant_be_used_for_more_than_one_function(self):
        self.view.GetFunction.return_value = "Func"
        self.view.GetModifier.return_value = "Ctrl"
        self.view.GetShortcutKey.return_value = "N"
        self.controller.on_apply_clicked(None)
        self.view.DisplayWarningMessage.assert_called_with(u"#The shortcut Ctrl+N is already bound to function 'File->New...'!#")

    def test_modifier_must_be_given_for_simple_key(self):
        self.view.GetFunction.return_value = "Func"
        self.view.GetModifier.return_value = ""
        self.view.GetShortcutKey.return_value = "N"
        self.controller.on_apply_clicked(None)
        self.view.DisplayWarningMessage.assert_called_with("#Both Modifier and Shortcut key must be given!#")

    def test_modifier_not_needed_for_function_keys(self):
        self.view.GetFunction.return_value = "Func"
        self.view.GetModifier.return_value = ""
        self.view.GetShortcutKey.return_value = "F1"
        self.controller.on_apply_clicked(None)
        self.assertEquals("Func", self.shortcut_config.function)
        self.assertEquals("F1", self.shortcut_config.shortcut)

    def test_modifier_must_be_known(self):
        self.view.GetFunction.return_value = "Func"
        self.view.GetModifier.return_value = "xxx"
        self.view.GetShortcutKey.return_value = "N"
        self.controller.on_apply_clicked(None)
        self.view.DisplayWarningMessage.assert_called_with("#Both Modifier and Shortcut key must be given!#")
