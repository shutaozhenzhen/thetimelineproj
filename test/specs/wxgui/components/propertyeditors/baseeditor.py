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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.components.propertyeditors.baseeditor import BaseEditor


class BaseEditorTestCase(UnitTestCase):

    def setUp(self):
        self.editor = Editor()
        self.base_editor = BaseEditor(None, self.editor)

    def tearDown(self):
        pass

    def given_base_editor_with_data(self):
        self.data = Mock(Data)
        self.base_editor.data = self.data

    def given_gui_editor(self):
        self.base_editor = Editor()


class describe_base_editor_instantiation(BaseEditorTestCase):

    def test_base_editor_can_be_instatiated(self):
        self.assertTrue(self.base_editor)

    def test_base_editor_has_no_data(self):
        self.assertEqual(self.base_editor.data, None)

    def test_base_editor_has_an_editor(self):
        self.assertEqual(self.base_editor.editor, self.editor)


class describe_base_editor_handles_data(BaseEditorTestCase):

    def test_data_can_be_set(self):
        self.given_base_editor_with_data()
        self.base_editor.set_data(1)
        self.assertTrue(self.data.SetValue.called_with(1))

    def test_data_can_be_retrieved(self):
        self.given_base_editor_with_data()
        _ = self.base_editor.get_data()
        self.assertTrue(self.data.GetValue.called)


class describe_base_editor_handles_focus(BaseEditorTestCase):

    def test_focus_is_set_when_data_exists(self):
        self.given_base_editor_with_data()
        self.base_editor.focus()
        self.assertTrue(self.data.SetFocus.called)

    def test_focus_is_not_set_when_no_data_exists(self):
        self.assertEqual(self.base_editor.data, None)
        # No exception thrown
        self.base_editor.focus()


class describe_gui_creation(BaseEditorTestCase):

    def test_superclass_gui_creation_functions_are_called(self):
        self.given_gui_editor()
        self.base_editor.create_gui()
        self.assertTrue(self.base_editor.create_sizer_called)
        self.assertTrue(self.base_editor.create_controls_called)
        self.assertTrue(self.base_editor.put_controls_in_sizer_called)
        self.assertTrue(self.base_editor.SetSizerAndFit_called)


class Editor(BaseEditor):

    def __init__(self):
        BaseEditor.__init__(self, None, self)
        self.create_sizer_called = False
        self.create_controls_called = False
        self.put_controls_in_sizer_called = False
        self.SetSizerAndFit_called = False

    def create_sizer(self):
        self.create_sizer_called = True

    def create_controls(self):
        self.create_controls_called = True

    def put_controls_in_sizer(self, sizer, controls):
        self.put_controls_in_sizer_called = True

    def SetSizerAndFit(self, sizer):
        self.SetSizerAndFit_called = True


class Data(object):

    def __init__(self):
        self.value = None

    def SetValue(self, value):
        self.value

    def GetValue(self):
        return self.value

    def SetFocus(self):
        pass
