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


from mock import Mock
import wx

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.internaltime import TimeDelta
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event
from timelinelib.wxgui.frames.mainframe.mainframe import AlertController
from timelinelib.wxgui.frames.mainframe.mainframe import MenuController


class describe_menu_controller(UnitTestCase):

    def test_menu_requiering_update_is_disabled_when_no_timeline_exists(self):
        self.given_menu_item_requires_update()
        self.given_no_timeline_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(False)

    def test_menu_requiering_update_is_enabled_when_timeline_is_updateable(self):
        self.given_menu_item_requires_update()
        self.given_timeline_is_updateable()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(True)

    def test_menu_requiering_update_is_disabledd_when_timeline_is_read_only(self):
        self.given_menu_item_requires_update()
        self.given_timeline_is_read_only()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(False)

    def test_menu_requiering_timeline_is_disabled_when_no_timeline_exists(self):
        self.given_menu_item_requires_timeline()
        self.given_no_timeline_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(False)

    def test_menu_requiering_timeline_is_enabled_when_timeline_exists(self):
        self.given_menu_item_requires_timeline()
        self.given_timeline_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(True)

    def test_menu_requiering_timeline_view_is_disabled_when_no_timeline_exists(self):
        self.given_menu_item_requires_timeline_view()
        self.given_no_timeline_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(False)

    def test_menu_requiering_timeline_view_is_disabled_when_no_timeline_view_exists(self):
        self.given_menu_item_requires_timeline_view()
        self.given_timeline_exists()
        self.given_no_timeline_view_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(False)

    def test_menu_requiering_timeline_view_is_enabled_when_timeline_view_exists(self):
        self.given_menu_item_requires_timeline_view()
        self.given_timeline_exists()
        self.given_timeline_view_exists()
        self.when_menu_state_possibly_has_changed()
        self.menu_item.Enable.assert_called_with(True)

    def setUp(self):
        self.menu_controller = MenuController()
        self.menu_item = Mock(wx.MenuItem)
        self.timeline = Mock(MemoryDB)
        self.menu_controller.on_timeline_change(self.timeline)
        self.timeline_panel_visible = False

    def given_menu_item_requires_update(self):
        self.menu_controller.add_menu_requiring_writable_timeline(self.menu_item)

    def given_menu_item_requires_timeline(self):
        self.menu_controller.add_menu_requiring_timeline(self.menu_item)

    def given_menu_item_requires_timeline_view(self):
        self.menu_controller.add_menu_requiring_visible_timeline_view(self.menu_item)

    def given_no_timeline_exists(self):
        self.menu_controller.on_timeline_change(None)

    def given_timeline_exists(self):
        self.menu_controller.on_timeline_change(self.timeline)

    def given_no_timeline_view_exists(self):
        self.timeline_panel_visible = False

    def given_timeline_view_exists(self):
        self.timeline_panel_visible = True

    def given_timeline_is_updateable(self):
        self.timeline.is_read_only.return_value = False

    def given_timeline_is_read_only(self):
        self.timeline.is_read_only.return_value = True

    def given_timeline_panel_is_visible(self):
        self.timeline_panel_visible = True

    def when_menu_state_possibly_has_changed(self):
        self.menu_controller.enable_disable_menus(self.timeline_panel_visible)


class describe_alert_controller(UnitTestCase):

    def test_alert_text_formatting(self):
        self.controller.time_type = GregorianTimeType()
        text = self.controller._format_alert_text(self.alert, self.event)
        expected_text = "Trigger time: %s\n\nEvent: %s\n\nTime to go" % (self.now, self.event.get_label(GregorianTimeType()))
        self.assertEqual(expected_text, text)

    def test_pytime_has_expired(self):
        self.given_early_pytimes()
        self.given_controller_time_type(GregorianTimeType())
        expired = self.controller._time_has_expired(self.tm)
        self.assertTrue(expired)

    def test_pytime_has_not_expired(self):
        self.given_late_pytimes()
        expired = self.controller._time_has_expired(self.tm)
        self.assertFalse(expired)

    def given_early_pytimes(self):
        self.given_pytime_now()
        self.given_pytime_earlier()
        self.given_controller_time_type(GregorianTimeType())
        self.alert = (self.now, "Time to go")

    def given_late_pytimes(self):
        self.given_pytime_now()
        self.given_pytime_later()
        self.given_controller_time_type(GregorianTimeType())
        self.alert = (self.now, "Time to go")

    def given_wxtime_later(self):
        self.tm = self.now + wx.TimeSpan(hours=12)

    def given_wxtime_earlier(self):
        self.tm = self.now - wx.TimeSpan(hours=12)

    def given_pytime_now(self):
        self.now = GregorianTimeType().now()

    def given_pytime_later(self):
        self.tm = self.now + TimeDelta.from_days(1)

    def given_pytime_earlier(self):
        self.tm = self.now + TimeDelta.from_days(-1)

    def given_controller_time_type(self, time_type):
        self.controller.time_type = time_type

    def setUp(self):
        self.now = GregorianTimeType().now()
        self.alert = (self.now, "Time to go")
        self.event = an_event()
        self.controller = AlertController()
