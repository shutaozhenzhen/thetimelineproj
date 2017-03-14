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


import os

from mock import Mock

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.event import Event
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.dialogs.slideshow.controller import SlideshowDialogController
from timelinelib.wxgui.dialogs.slideshow.view import SlideshowDialog


PATH = "c:\\temp\\zyx"
FILE = "foo.txt"


class describe_slideshow_dialog_controller(UnitTestCase):

    def test_is_initialized(self):
        self.assertEqual(self.db, self.controller._db)
        self.assertEqual(self.canvas, self.controller._canvas)
        self.assertFalse(self.controller._text_transformer is None)

    def test_user_can_select_target_directory(self):
        self.simuate_user_selects_directory()
        self.view.ChangeDir.assert_called_with()

    def test_target_directory_is_mandatory(self):
        self.view.GetTargetDir.return_value = ""
        self.simuate_user_clicks_ok()
        self.view.InvalidTargetDir.assert_called_with("#The html pages directory is mandatory#")

    def test_creation_of_target_directory_can_be_rejected(self):
        self.view.GetTargetDir.return_value = PATH
        self.view.GetUserAck.return_value = False
        self.simuate_user_clicks_ok()
        self.assertFalse(os.path.exists(PATH))
        self.assertEqual(0, self.view.EndModalOk.call_count)

    def test_creation_of_target_directory_can_be_accepted(self):
        vp = Mock()
        vp.filter_events.return_value = []
        self.canvas.get_view_properties.return_value = vp
        self.view.GetTargetDir.return_value = PATH
        self.view.GetUserAck.return_value = True
        self.simuate_user_clicks_ok()
        self.assertTrue(os.path.exists(PATH))
        self.view.EndModalOk.assert_called_with()

    def test_overwrite_of_target_directory_can_be_rejected(self):
        vp = Mock()
        vp.filter_events.return_value = []
        self.canvas.get_view_properties.return_value = vp
        os.mkdir(PATH)
        f = open(os.path.join(PATH, FILE), "w")
        f.close()
        self.view.GetTargetDir.return_value = PATH
        self.view.GetUserAck.return_value = False
        self.simuate_user_clicks_ok()
        self.assertTrue(os.path.exists(PATH))
        self.assertEqual(0, self.view.EndModalOk.call_count)

    def test_overwrite_of_target_directory_can_be_accepted(self):
        event = Event(start_time=human_time_to_gregorian("11 Jul 2014"),
                      end_time=human_time_to_gregorian("12 Jul 2014"),
                      text="a day in my life")
        vp = Mock()
        vp.filter_events.return_value = [event, ]
        self.canvas.get_view_properties.return_value = vp
        os.mkdir(PATH)
        f = open(os.path.join(PATH, FILE), "w")
        f.close()
        self.view.GetTargetDir.return_value = PATH
        self.view.GetUserAck.return_value = True
        self.simuate_user_clicks_ok()
        self.assertTrue(os.path.exists(PATH))
        self.view.DisplayStartPage.assert_called_with(os.path.join(PATH, "page_1.html"))
        self.view.EndModalOk.assert_called_with()

    def simulate_dialog_init(self, db, canvas):
        self.controller.on_init(db, canvas)

    def simuate_user_selects_directory(self):
        evt = Mock()
        self.controller.on_change_dir(evt)

    def simuate_user_clicks_ok(self):
        evt = Mock()
        self.controller.on_start(evt)

    def setUp(self):
        self.db = Mock(MemoryDB)
        self.db.time_type = GregorianTimeType()
        self.start_time = human_time_to_gregorian("1 Jan 2010")
        self.canvas = Mock()
        self.view = self._mock_view()
        self.controller = SlideshowDialogController(self.view)
        self.simulate_dialog_init(self.db, self.canvas)
        if not os.path.exists("c:\\temp"):
            os.mkdir("c:\\temp")

    def tearDown(self):
        if os.path.exists(PATH):
            files = os.listdir(PATH)
            for f in files:
                os.remove(os.path.join(PATH, f))
            os.rmdir(PATH)

    def _mock_view(self):
        view = Mock(SlideshowDialog)
        view.AllEventsSelected.return_value = False
        view.GetTargetDir.return_value = ""
        return view
