# -*- coding: utf-8 -*-
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

from timelinelib.utilities.encodings import to_unicode
from timelinelib.wxgui.dialogs.feedback.feedbackdialogcontroller import FeedbackDialogController
from timelinelib.wxgui.dialogs.feedback.feedbackdialog import FeedbackDialog
from timelinetest import UnitTestCase


class FeedbackDialogControllerSpec(UnitTestCase):

    def test_shows_parts_in_dialog(self):
        self.form.populate(info="info text", subject="subject text", body="body text")
        self.dialog.set_info_text.assert_called_with("info text")
        self.dialog.set_subject_text.assert_called_with("subject text")
        self.dialog.set_body_text.assert_called_with("body text")

    def test_can_send_with_default(self):
        self.dialog.get_to_text.return_value = "foo@example.com"
        self.dialog.get_subject_text.return_value = "sub ject"
        self.dialog.get_body_text.return_value = "bo dy"
        self.form.send_with_default()
        self.webbrowser.open.assert_called_with("mailto:foo%40example.com?subject=sub%20ject&body=bo%20dy")

    def test_can_send_unicode_characters(self):
        self.dialog.get_to_text.return_value = "foo@example.com"
        self.dialog.get_subject_text.return_value = "subject"
        self.dialog.get_body_text.return_value = to_unicode("åäöÅÄÖ")
        self.form.send_with_default()
        self.webbrowser.open.assert_called_with("mailto:foo%40example.com?subject=subject&body=%C3%A5%C3%A4%C3%B6%C3%85%C3%84%C3%96")

    def test_can_send_with_gmail(self):
        self.dialog.get_to_text.return_value = "foo@example.com"
        self.dialog.get_subject_text.return_value = "sub ject"
        self.dialog.get_body_text.return_value = "bo dy"
        self.form.send_with_gmail()
        self.webbrowser.open.assert_called_with("https://mail.google.com/mail/?compose=1&view=cm&fs=1&to=foo%40example.com&su=sub%20ject&body=bo%20dy")

    def setUp(self):
        self.dialog = Mock(FeedbackDialog)
        self.webbrowser = Mock()
        self.form = FeedbackDialogController(self.dialog, self.webbrowser)
