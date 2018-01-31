#!/usr/bin/env python

import wx
import os.path


COPYRIGHT = """\
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


"""

IMPORTS = """\
from timelinelib.wxgui.dialogs.%s.controller import %sController
from timelinelib.wxgui.framework import Dialog


"""

TEST_IMPORTS = """\
from mock import Mock

from timelinelib.wxgui.dialogs.%s.controller import %sController
from timelinelib.wxgui.dialogs.%s.view import %s
from timelinelib.test.cases.unit import UnitTestCase


"""


DIALOG = """\
class %s(Dialog):

    \"\"\"
    <BoxSizerVertical>
        <Button label="$(test_text)" />
    </BoxSizerVertical>
    \"\"\"

    def __init__(self, parent):
        Dialog.__init__(self, %sController, parent, {
            "test_text": "Hello World",
        }, title=_("New dialog title"))
        self.controller.on_init()
"""


CONTROLLER = """\
from timelinelib.wxgui.framework import Controller


class %sController(Controller):

    def on_init(self):
        pass
"""

TEST = """\
class describe_%s(UnitTestCase):

    def setUp(self):
        self.view = Mock(%s)
        self.controller = %sController(self.view)

    def test_it_can_be_created(self):
        self.show_dialog(%s, None)
"""


def write_file(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()


def ensure_package_exists(package_path):
    if not os.path.exists(package_path):
        os.makedirs(package_path)
        write_file(os.path.join(package_path, "__init__.py"), "")


def get_user_ack(question):
    return wx.MessageBox(question, "Question",
                         wx.YES_NO | wx.CENTRE | wx.NO_DEFAULT) == wx.YES


def write_python_module(path, content):
    if os.path.exists(path):
        if not get_user_ack("Module %s already exists\nOverwrite?" % path):
            return
    ensure_package_exists(os.path.dirname(path))
    write_file(path, content)


def create_dialog_test_file(path, file_name, class_name):
    write_python_module(
        os.path.join(path, file_name + ".py"),
        "".join([
            COPYRIGHT,
            TEST_IMPORTS % (file_name, class_name, file_name, class_name),
            TEST % (class_name, class_name, class_name, class_name),
        ])
    )


def create_dialog_controller_file(path, file_name, class_name):
    write_python_module(
        os.path.join(path, "controller.py"),
        "".join([
            COPYRIGHT,
            CONTROLLER % class_name,
        ])
    )


def create_dialog_view_file(path, file_name, class_name):
    write_python_module(
        os.path.join(path, "view.py"),
        "".join([
            COPYRIGHT,
            IMPORTS % (file_name, class_name),
            DIALOG % (class_name, class_name),
        ])
    )


def remove_postfix(postfix, text):
    if text.endswith(postfix):
        return text[:-len(postfix)]
    else:
        return text


def base_file_name_from_class_name(class_name):
    return remove_postfix("dialog", class_name.lower().replace("_", ""))


def create_py_files(class_name):
    file_name = base_file_name_from_class_name(class_name)
    source_path = os.path.join(os.getcwd(), "source", "timelinelib", "wxgui", "dialogs", file_name)
    test_path = os.path.join(os.getcwd(), "test", "specs", "wxgui", "dialogs")
    create_dialog_view_file(source_path, file_name, class_name)
    create_dialog_controller_file(source_path, file_name, class_name)
    create_dialog_test_file(test_path, file_name, class_name)


def get_class_name():
    dlg = wx.TextEntryDialog(None, "Enter the class name:", "Create a Dialog class", "")
    if dlg.ShowModal() == wx.ID_OK:
        return dlg.GetValue()
    else:
        raise Exception("Name is mandatory")


def execute():
    app = wx.App()
    app.MainLoop()
    try:
        class_name = get_class_name()
        if class_name == "":
            raise Exception("Name can't be empty")
        create_py_files(class_name)
    except Exception, ex:
        print ex
        pass
        print "None"


if __name__ == "__main__":
    execute()
