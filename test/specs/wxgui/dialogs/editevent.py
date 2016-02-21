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
from mock import sentinel

from timelinelib.calendar.defaultdateformatter import DefaultDateFormatter
from timelinelib.canvas.data.container import Container
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.event import Event
from timelinelib.canvas.data.subevent import Subevent
from timelinelib.config.dotfile import Config
from timelinelib.db import db_open
from timelinelib.repositories.interface import EventRepository
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.test.utils import ObjectWithTruthValue
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.wxgui.dialogs.editevent.controller import EditEventDialogController
from timelinelib.wxgui.dialogs.editevent.view import EditEventDialog


class EditEventDialogTestCase(UnitTestCase):

    def setUp(self):
        self.view = Mock(EditEventDialog)
        self.controller = EditEventDialogController(self.view)
        self.event_repository = Mock(EventRepository)
        self.db = MemoryDB()
        self.config = Mock(Config)
        self.config.event_editor_show_period = False
        self.config.event_editor_show_time = False

    def when_show_period_used_last_time(self):
        self.config.event_editor_show_period = True

    def when_show_period_not_used_last_time(self):
        self.config.event_editor_show_period = False

    def when_show_time_used_last_time(self):
        self.config.event_editor_show_time = True

    def when_show_time_not_used_last_time(self):
        self.config.event_editor_show_time = False

    def when_editing_a_new_event(self):
        self.when_editor_opened_with_time("1 Jan 2010")

    def when_editor_opened_with_time(self, time, event=None):
        self.when_editor_opened_with(
            human_time_to_gregorian(time), human_time_to_gregorian(time), event)

    def when_editor_opened_with_period(self, start, end):
        self.when_editor_opened_with(
            human_time_to_gregorian(start), human_time_to_gregorian(end), None)

    def when_editor_opened_with_event(self, event):
        self.when_editor_opened_with(None, None, event)

    def when_editor_opened_with(self, start, end, event):
        self.controller.on_init(
            self.config,
            GregorianTimeType(),
            self.event_repository,
            self.db,
            start,
            end,
            event)

    def simulate_user_enters_start_time(self, time):
        self.view.GetStart.return_value = human_time_to_gregorian(time)

    def simulate_user_enters_end_time(self, time):
        self.view.GetEnd.return_value = human_time_to_gregorian(time)

    def simulate_user_clicks_ok(self):
        self.controller.on_ok_clicked(None)

    def simulate_user_selects_a_container(self, subevent):
        container = Container(GregorianTimeType(), subevent.time_period.start_time, subevent.time_period.start_time, "container")
        container.register_subevent(subevent)
        self.controller.container = container

    def simulate_ends_today_checked(self, today):
        self.controller.end = today

    def assert_start_time_set_to(self, time):
        self.view.SetStart.assert_called_with(human_time_to_gregorian(time))

    def assert_end_time_set_to(self, time):
        self.view.SetEnd.assert_called_with(human_time_to_gregorian(time))

    def assert_no_event_saved(self):
        self.assertFalse(self.event_repository.save.called)
        self.assertFalse(self.view.EndModal.called)
        self.assertFalse(self.view.ClearEventData.called)


class describe_edit_event_dialog(EditEventDialogTestCase):

    def test_it_can_be_created(self):
        config = Mock(Config)
        config.get_date_format.return_value = "yyyy-mm-dd"
        config.event_editor_show_period = True
        config.event_editor_show_time = False
        config.event_editor_tab_order = ["0", "1", "2", "3", "4", ":"]
        config.get_gregorian_date_formatter.return_value = DefaultDateFormatter()
        db = db_open(":tutorial:")
        categories = db.get_categories()
        categories[0].parent = categories[1]
        db.save_category(categories[0])
        self.show_dialog(EditEventDialog, None, config, "title", db)

    def test_it_can_be_created_with_numeric_timeline(self):
        config = Mock(Config)
        config.get_date_format.return_value = "yyyy-mm-dd"
        config.event_editor_show_period = True
        config.event_editor_show_time = False
        config.event_editor_tab_order = ["0", "1", "2", "3", "4", ":"]
        db = db_open(":numtutorial:")
        categories = db.get_categories()
        categories[0].parent = categories[1]
        db.save_category(categories[0])
        self.show_dialog(EditEventDialog, None, config, "title", db)


class describe_start_time_field(EditEventDialogTestCase):

    def test_has_value_from_first_argument(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.assert_start_time_set_to("1 Jan 2010")

    def test_has_value_from_event(self):
        time_period = Mock()
        time_period.start_time = sentinel.START_TIME
        event = Mock()
        event.get_time_period.return_value = time_period
        self.when_editor_opened_with_event(event)
        self.view.SetStart.assert_called_with(sentinel.START_TIME)


class describe_end_time_field(EditEventDialogTestCase):

    def test_has_value_from_first_argument_if_only_one_given(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.assert_end_time_set_to("1 Jan 2010")

    def test_has_value_from_second_argument(self):
        self.when_editor_opened_with_period("1 Jan 2010", "2 Jan 2010")
        self.assert_end_time_set_to("2 Jan 2010")

    def test_has_value_from_event(self):
        time_period = Mock()
        time_period.end_time = sentinel.END_TIME
        event = Mock()
        event.get_time_period.return_value = time_period
        self.when_editor_opened_with_event(event)
        self.view.SetEnd.assert_called_with(sentinel.END_TIME)

    def test_is_hidden_if_no_period(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.SetShowPeriod.assert_called_with(False)

    def test_is_shown_if_shown_previous_time(self):
        self.when_show_period_used_last_time()
        self.when_editor_opened_with_period("1 Jan 2010", "2 Jan 2010")
        self.view.SetShowPeriod.assert_called_with(True)

    def test_is_shown_if_period_defined(self):
        self.when_show_period_not_used_last_time()
        self.when_editor_opened_with_period("1 Jan 2010", "2 Jan 2010")
        self.view.SetShowPeriod.assert_called_with(True)


class describe_time_fields(EditEventDialogTestCase):

    def test_are_hidden_if_no_time_specified(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.SetShowTime.assert_called_with(False)

    def test_are_shown_if_shown_previous_time(self):
        self.when_show_time_used_last_time()
        self.when_editor_opened_with_time("1 Jan 2010 15:30")
        self.view.SetShowTime.assert_called_with(True)

    def test_are_not_shown_if_not_shown_previous_time(self):
        self.when_show_time_not_used_last_time()
        self.when_editor_opened_with_time("1 Jan 2010 15:30")
        self.view.SetShowTime.assert_called_with(True)


class describe_fuzzy_checkbox(EditEventDialogTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetFuzzy.assert_called_with(False)

    def test_has_value_from_event(self):
        event = Mock()
        event.get_fuzzy.return_value = sentinel.FUZZY
        self.when_editor_opened_with_event(event)
        self.view.SetFuzzy.assert_called_with(sentinel.FUZZY)


class describe_locked_checkbox(EditEventDialogTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetLocked.assert_called_with(False)

    def test_has_value_from_event(self):
        event = Mock()
        event.get_locked.return_value = sentinel.LOCKED
        self.when_editor_opened_with_event(event)
        self.view.SetLocked.assert_called_with(sentinel.LOCKED)


class describe_start_is_in_history(EditEventDialogTestCase):

    def test_new_event_starts_in_history(self):
        time = "1 Jan 3010"
        self.when_editor_opened_with_time("1 Jan 3010", Event(GregorianTimeType(), human_time_to_gregorian(time), human_time_to_gregorian(time), ""))
        self.assertFalse(self.controller._start_is_in_history())

    def test_new_event_starting_in_history(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.assertTrue(self.controller._start_is_in_history())

    def test_event_not_starting_in_history(self):
        time_period = Mock()
        time_period.start_time = human_time_to_gregorian("1 Jan 3010")
        event = Mock()
        event.get_time_period.return_value = time_period
        self.when_editor_opened_with_event(event)
        self.assertFalse(self.controller._start_is_in_history())

    def test_event_starting_in_history(self):
        time_period = Mock()
        time_period.start_time = human_time_to_gregorian("1 Jan 2010")
        event = Mock()
        event.get_time_period.return_value = time_period
        self.when_editor_opened_with_event(event)
        self.assertTrue(self.controller._start_is_in_history())


class describe_ends_today_checkbox(EditEventDialogTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetEndsToday.assert_called_with(False)

    def test_has_value_from_event(self):
        event = Mock()
        event.get_ends_today.return_value = sentinel.ENDS_TODYAY
        self.when_editor_opened_with_event(event)
        self.view.SetEndsToday.assert_called_with(sentinel.ENDS_TODYAY)

    def test_no_endtime_check(self):
        self.when_editor_opened_with_period("2 Jan 2010", "3 Jan 2010")
        self.controller.ends_today = True
        end_time = human_time_to_gregorian("1 Jan 2010")
        self.assertTrue(end_time <= self.controller._validate_and_save_end(end_time))


class describe_text_field(EditEventDialogTestCase):

    def test_has_no_value_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetName.assert_called_with("")

    def test_has_value_from_event(self):
        event = Mock()
        event.get_text.return_value = sentinel.TEXT
        self.when_editor_opened_with_event(event)
        self.view.SetName.assert_called_with(sentinel.TEXT)


class describe_category_field(EditEventDialogTestCase):

    def test_has_no_value_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetCategory.assert_called_with(None)

    def test_has_value_from_event(self):
        event = Mock()
        event.get_category.return_value = sentinel.CATEGORY
        self.when_editor_opened_with_event(event)
        self.view.SetCategory.assert_called_with(sentinel.CATEGORY)


class describe_additional_data(EditEventDialogTestCase):

    def test_is_populated_from_event(self):
        event = Mock()
        event.data = sentinel.DATA
        self.when_editor_opened_with_event(event)
        self.view.SetEventData.assert_called_with(sentinel.DATA)

    def test_is_not_set_for_new_events(self):
        self.when_editing_a_new_event()
        self.assertFalse(self.view.SetEventData.called)


class describe_add_more_checkbox(EditEventDialogTestCase):

    def test_is_hidden_when_editing_existing_event(self):
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))
        self.view.SetShowAddMoreCheckbox.assert_called_with(False)

    def test_is_shown_when_editing_new_event(self):
        self.when_editing_a_new_event()
        self.view.SetShowAddMoreCheckbox.assert_called_with(True)


class describe_saving(object):

    def given_saving_valid_event(self):
        self.locked_value = ObjectWithTruthValue(False)
        self.ends_today_value = ObjectWithTruthValue(False)
        self.simulate_user_enters_start_time("1 Jan 2010")
        self.simulate_user_enters_end_time("2 Jan 2010")
        self.view.GetFuzzy.return_value = sentinel.FUZZY
        self.view.GetLocked.return_value = self.locked_value
        self.view.GetEndsToday.return_value = self.ends_today_value
        self.view.GetName.return_value = "new event"
        self.view.GetCategory.return_value = sentinel.CATEGORY
        self.view.GetEventData.return_value = sentinel.EVENT_DATA
        self.view.GetContainer.return_value = None
        self.simulate_user_clicks_ok()
        self.saved_event = self.event_repository.save.call_args[0][0]

    def test_saves_start_time(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_time_period().start_time,
                         human_time_to_gregorian("1 Jan 2010"))

    def test_saves_end_time(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_time_period().end_time,
                         human_time_to_gregorian("2 Jan 2010"))

    def test_saves_end_time_from_start_time(self):
        self.view.GetShowPeriod.return_value = False
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_time_period().end_time,
                         human_time_to_gregorian("1 Jan 2010"))

    def test_saves_text(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_text(), "new event")

    def test_saves_category(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_category(), sentinel.CATEGORY)

    def test_saves_fuzzy(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_fuzzy(), sentinel.FUZZY)

    def test_saves_locked(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_locked(), self.locked_value)

    def test_saves_ends_today(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.get_ends_today(), self.ends_today_value)

    def test_saves_data(self):
        self.given_saving_valid_event()
        self.assertEqual(self.saved_event.data, sentinel.EVENT_DATA)


class describe_saving_new(EditEventDialogTestCase, describe_saving):

    def setUp(self):
        EditEventDialogTestCase.setUp(self)
        self.when_editing_a_new_event()


class describe_saving_existing(EditEventDialogTestCase, describe_saving):

    def setUp(self):
        EditEventDialogTestCase.setUp(self)
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))


class describe_validation(EditEventDialogTestCase):

    def test_start_must_be_valid(self):
        self.when_editing_a_new_event()
        self.view.GetStart.side_effect = ValueError
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidStart.called)
        self.assert_no_event_saved()

    def test_end_must_be_valid(self):
        self.when_editing_a_new_event()
        self.view.GetEnd.side_effect = ValueError
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidEnd.called)
        self.assert_no_event_saved()

    def test_start_must_be_less_then_end(self):
        self.when_editor_opened_with_period("1 Jan 2010", "1 Jan 2010")
        self.view.GetName.return_value = "updated_event"
        self.view.GetEndsToday.return_value = False
        self.simulate_user_enters_start_time("2 Jan 2011")
        self.simulate_user_enters_end_time("1 Jan 2011")
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidStart.called)
        self.assert_no_event_saved()

    def test_period_can_be_long(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.GetName.return_value = "a valid name"  # why needed?
        self.view.GetLocked.return_value = False  # why needed?
        self.view.GetEndsToday.return_value = False
        self.simulate_user_enters_start_time("1 Jan 2000")
        self.simulate_user_enters_end_time("1 Jan 5000")
        self.simulate_user_clicks_ok()
        self.assertEqual(0, self.view.DisplayErrorMessage.call_count)

    def test_time_cant_change_when_event_is_locked(self):
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))
        self.simulate_user_enters_start_time("2 Jan 2011 12:00")
        self.simulate_user_enters_end_time("1 Jan 2011 12:00")
        self.view.GetLocked.return_value = True
        self.simulate_user_clicks_ok()
        self.view.DisplayInvalidStart.assert_called_with(
            _("You can't change time when the Event is locked"))
        self.assert_no_event_saved()


class describe_ends_today_in_container(EditEventDialogTestCase):

    def test_set_ends_today_on_subevent_extends_container_period(self):
        start = human_time_to_gregorian("1 Jan 2010")
        today = human_time_to_gregorian("1 Jan 2015")
        subevent = Subevent(GregorianTimeType(), start, start, "subevent")
        self.when_editor_opened_with_event(subevent)
        self.simulate_user_selects_a_container(subevent)
        self.simulate_ends_today_checked(today)
        self.controller._update_event()
        self.assertEqual(self.controller.container.time_period.end_time, today)
