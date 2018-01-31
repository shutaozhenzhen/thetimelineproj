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


import humblewx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.framework import Dialog


class describe_message_bar_component(UnitTestCase):

    def test_it_shows_in_dialog(self):
        self.show_dialog(TestDialog)


class TestDialog(Dialog):

    """
    <BoxSizerVertical>
        <BoxSizerHorizontal>
            <Button
                label="Hide"
                event_EVT_BUTTON="on_hide"
            />
            <Button
                label="Show information"
                event_EVT_BUTTON="on_show_information"
            />
            <Button
                label="Show warning"
                event_EVT_BUTTON="on_show_warning"
            />
        </BoxSizerHorizontal>
        <StaticText label="---- separator ----" />
        <MessageBar name="information" />
        <StaticText label="---- separator ----" />
        <MessageBar name="warning" />
        <StaticText label="---- separator ----" />
    </BoxSizerVertical>
    """

    class Controller(humblewx.Controller):

        INFORMATION_TEXT = "This is an\ninformation message."
        WARNING_TEXT = "This is a\nwarning message!"

        def on_init(self):
            self.view.information.ShowInformationMessage(self.INFORMATION_TEXT)
            self.view.warning.ShowWarningMessage(self.WARNING_TEXT)
            self.view.SetSizerAndFit(self.view.GetSizer())

        def on_hide(self, event):
            self.view.information.ShowNoMessage()

        def on_show_information(self, event):
            self.view.information.ShowInformationMessage(self.INFORMATION_TEXT)

        def on_show_warning(self, event):
            self.view.information.ShowWarningMessage(self.WARNING_TEXT)

    def __init__(self):
        Dialog.__init__(self, self.Controller, None, {
        })
        self.controller.on_init()
