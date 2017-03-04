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

from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.num.timetype import NumTimeType
from timelinelib.canvas.data.container import Container
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data.event import Event
from timelinelib.canvas.data.internaltime import delta_from_days
from timelinelib.canvas.data.subevent import Subevent
from timelinelib.config.dotfile import Config
from timelinelib.db import db_open
from timelinelib.repositories.interface import EventRepository
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.test.utils import ObjectWithTruthValue
from timelinelib.wxgui.dialogs.editevent.controller import EditEventDialogController
from timelinelib.wxgui.dialogs.editevent.view import EditEventDialog


class EditEventDialogTestCase(UnitTestCase):

    def setUp(self):
        self.view = Mock(EditEventDialog)
        self.controller = EditEventDialogController(self.view)
        self.event_repository = Mock(EventRepository)
        self.db = MemoryDB()
        self.num_db = MemoryDB()
        self.num_db.time_type = NumTimeType()
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
        self.view.GetEndsToday.return_value = False

    def when_editor_opened_with_time(self, time, event=None):
        self.when_editor_opened_with(
            human_time_to_gregorian(time), human_time_to_gregorian(time), event)

    def when_editor_opened_with_period(self, start, end):
        self.when_editor_opened_with(
            human_time_to_gregorian(start), human_time_to_gregorian(end), None)

    def when_editor_opened_with_event(self, event):
        self.when_editor_opened_with(None, None, event)

    def when_editor_opened_with_num_event(self, event):
        self.when_editor_opened_with_num(None, None, event)

    def when_editor_opened_with(self, start, end, event):
        self.controller.on_init(
            self.config,
            GregorianTimeType(),
            self.event_repository,
            self.db,
            start,
            end,
            event)
        self.view.GetStart.return_value = start
        self.view.GetEnd.return_value = end
        self.view.GetContainer.return_value = None
        self.view.IsAddMoreChecked.return_value = False

    def when_editor_opened_with_num(self, start, end, event):
        self.controller.on_init(
            self.config,
            NumTimeType(),
            self.event_repository,
            self.num_db,
            start,
            end,
            event)

    def simulate_user_enters_start_time(self, time):
        self.view.GetStart.return_value = human_time_to_gregorian(time)

    def simulate_user_enters_end_time(self, time):
        self.view.GetEnd.return_value = human_time_to_gregorian(time)

    def simulate_user_enters_num_start_time(self, time):
        self.view.GetStart.return_value = time

    def simulate_user_enters_num_end_time(self, time):
        self.view.GetEnd.return_value = time

    def simulate_user_clicks_ok(self):
        self.controller.on_ok_clicked(None)

    def simulate_user_clicks_save_and_duplicate(self):
        self.controller.on_duplicate(Mock())

    def simulate_user_checkes_locked_checkbox(self):
        evt = Mock()
        self.view.GetContainer.return_value = None
        self.view.GetLocked.return_value = False
        self.controller.on_locked_checkbox_changed(evt)

    def simulate_user_uncheckes_locked_checkbox(self):
        evt = Mock()
        self.view.GetContainer.return_value = None
        self.view.GetLocked.return_value = True
        self.controller.on_locked_checkbox_changed(evt)

    def simulate_user_checkes_show_time_checkbox(self):
        event = Mock()
        event.IsChecked.return_value = True
        self.controller.on_show_time_checkbox_changed(event)

    def simulate_user_uncheckes_show_time_checkbox(self):
        event = Mock()
        event.IsChecked.return_value = False
        self.controller.on_show_time_checkbox_changed(event)

    def simulate_container_changed(self):
        evt = Mock()
        self.controller.on_container_changed(evt)

    def simulate_user_clicks_period_checkbox(self, checked=True):
        event = Mock()
        event.IsChecked.return_value = checked
        self.controller.on_period_checkbox_changed(event)

    def simulate_user_selects_a_container(self, subevent):
        time_period = subevent.get_time_period()
        container = Container(time_period.start_time, time_period.start_time, "container")
        container.register_subevent(subevent)
        self.controller.container = container

    def simulate_ends_today_checked(self, today):
        self.controller.end = today

    def simulate_user_clicks_enlarge_button(self, enlarged=True):
        import wx
        app = wx.App()
        evt = Mock()
        if enlarged:
            self.controller.reduced_size = sentinel.REDUCE_SIZE
            self.controller.reduced_pos = sentinel.REDUCE_POS
            self.controller.on_reduce_click(evt)
        else:
            self.controller.on_enlarge_click(evt)
        app.Destroy()

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
        config.get_date_formatter.return_value = GregorianDateFormatter()
        config.event_editor_show_period = True
        config.event_editor_show_time = False
        config.event_editor_tab_order = ["0", "1", "2", "3", "4", ":"]
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

    def test_show_time_click_changes_view(self):
        self.simulate_user_checkes_show_time_checkbox()
        self.view.SetShowTime.assert_called_with(True)
        self.simulate_user_uncheckes_show_time_checkbox()
        self.view.SetShowTime.assert_called_with(False)


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

    def test_when_locked_checked_view_changes(self):
        self.when_editing_a_new_event()
        self.simulate_user_checkes_locked_checkbox()
        self.view.EnableEndsToday.assert_called_with(True)
        self.simulate_user_uncheckes_locked_checkbox()
        self.view.EnableEndsToday.assert_called_with(False)

    def test_enable_disable_locked(self):
        self.controller.event = Mock()
        self.controller.event.is_container.return_value = False
        self.controller._enable_disable_locked(True)
        self.view.EnableLocked.assert_called_with(True)


class describe_start_is_in_history(EditEventDialogTestCase):

    def test_new_event_starts_in_history(self):
        time = "1 Jan 3010"
        self.when_editor_opened_with_time("1 Jan 3010", Event(human_time_to_gregorian(time), human_time_to_gregorian(time), ""))
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

    def test_dialog_closes_after_saving(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.IsAddMoreChecked.return_value = False
        self.controller.opened_from_menu = False
        self.simulate_user_clicks_ok()
        self.view.EndModalOk.assert_called_with()

    def test_dialog_closes_after_saving_and_pos_size_data_saved_to_config(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.IsAddMoreChecked.return_value = False
        self.controller.opened_from_menu = True
        self.simulate_user_clicks_ok()
        self.view.GetShowPeriod.assert_called_with()
        self.view.GetShowTime.assert_called_with()
        self.view.EndModalOk.assert_called_with()


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
        subevent = Subevent(start, start, "subevent")
        self.when_editor_opened_with_event(subevent)
        self.simulate_user_selects_a_container(subevent)
        self.simulate_ends_today_checked(today)
        self.controller._update_event()
        self.assertTrue(self.controller.container.get_time_period().ends_at(today))

    def test_container_allows_ends_today(self):
        self.view.GetContainer.return_value = None
        self.assertTrue(self.controller._container_allows_ends_today())

    def test_start_is_in_history(self):
        self.controller.event = Mock()
        self.controller.start = None
        self.assertFalse(self.controller._start_is_in_history())

    def test_update_event_delete(self):
        self.when_editing_a_new_event()
        self.controller.container = Mock()
        self.controller.event = Mock()
        self.controller.timeline = Mock()
        self.controller.timeline.get_containers.return_value = []
        self.controller.event.is_subevent.return_value = False
        self.controller._update_event()
        self.assertEqual(1, self.controller.timeline.delete_event.call_count)

    def test_update_event_register(self):
        self.when_editing_a_new_event()
        self.controller.container = Mock()
        self.controller.event = Mock()
        self.controller.event.container = Mock()
        self.controller.timeline = Mock()
        self.controller.timeline.get_containers.return_value = []
        self.controller.event.is_subevent.return_value = True
        self.controller._update_event()
        self.controller.container.register_subevent.asert_called_with(self.controller.event)

    def test_update_event_(self):
        self.when_editing_a_new_event()
        self.controller.container = None
        self.controller.event = Mock()
        self.controller.timeline = Mock()
        self.controller.event.is_subevent.return_value = True
        self.controller._update_event()
        self.assertEqual(1, self.controller.timeline.delete_event.call_count)


class describe_period_selection(EditEventDialogTestCase):

    def test_period_can_be_turned_on_for_datetime_timeline(self):
        event = Mock()
        self.when_editor_opened_with_event(event)
        self.simulate_user_enters_start_time("1 Jan 2010")
        self.simulate_user_enters_end_time("1 Jan 2010")
        self.simulate_user_clicks_period_checkbox(sentinel.STATE)
        self.view.ShowToTime.assert_called_with(sentinel.STATE)
        self.view.SetEnd.assert_called_with(self.view.GetStart() + delta_from_days(1))

    def test_period_can_be_turned_on_even_when_end_time_type_is_unexpected(self):
        event = Mock()
        self.when_editor_opened_with_event(event)
        self.simulate_user_enters_start_time("1 Jan 2010")
        self.simulate_user_enters_end_time("1 Jan 2010")
        self.view.SetEnd.side_effect = TypeError()
        self.simulate_user_clicks_period_checkbox(sentinel.STATE)
        self.view.ShowToTime.assert_called_with(sentinel.STATE)

    def test_period_can_be_turned_on_for_numtime_timeline(self):
        event = Mock()
        self.when_editor_opened_with_num_event(event)
        self.simulate_user_enters_num_start_time(1)
        self.simulate_user_enters_num_end_time(1)
        self.simulate_user_clicks_period_checkbox(sentinel.STATE)
        self.view.ShowToTime.assert_called_with(sentinel.STATE)
        self.view.SetEnd.assert_called_with(2)


class describe_enlarging(EditEventDialogTestCase):

    def test_enlarging_click_changes_pos_and_size(self):
        self.when_editing_a_new_event()
        self.simulate_user_clicks_enlarge_button(enlarged=False)
        self.assertEqual(1, self.view.SetPosition.call_count)
        self.assertEqual(1, self.view.SetSize.call_count)

    def _test_reduce_click_changes_pos_and_size(self):
        self.when_editing_a_new_event()
        self.simulate_user_clicks_enlarge_button(enlarged=True)
        self.view.SetPosition.assert_called_with(sentinel.REDUCE_POS)
        self.view.SetSize.assert_called_with(sentinel.REDUCE_SIZE)


class describe_changing_container(EditEventDialogTestCase):

    def test(self):
        self.when_editing_a_new_event()
        self.simulate_container_changed()
        self.assertEqual(1, self.view.EnableEndsToday.call_count)
        self.assertEqual(1, self.view.EnableLocked.call_count)

    def test_max_cid(self):
        MAX_CID = 99
        container = Mock()
        container.cid.return_value = MAX_CID - 1
        self.controller.timeline = Mock()
        self.controller.timeline.get_containers.return_value = [container]
        self.controller.container = container
        self.controller._add_new_container()
        container.set_cid.assert_called_with(MAX_CID)


class describe_exceptions(EditEventDialogTestCase):

    def test_start_changed(self):
        self.when_editing_a_new_event()
        self.controller.start = human_time_to_gregorian("1 Jan 2010")
        self.controller.end = human_time_to_gregorian("1 Jan 2010")
        start = human_time_to_gregorian("1 Jan 2009")
        try:
            self.controller._verify_that_time_has_not_been_changed(start, self.controller.end)
            self.fail("Unexpected ok")
        except ValueError:
            self.view.SetStart.assert_called_with(self.controller.start)
            self.view.DisplayInvalidStart.assert_called_with("#You can't change time when the Event is locked#")

    def test_end_changed(self):
        self.when_editing_a_new_event()
        self.controller.start = human_time_to_gregorian("1 Jan 2010")
        self.controller.end = human_time_to_gregorian("1 Jan 2010")
        end = human_time_to_gregorian("1 Jan 2011")
        try:
            self.controller._verify_that_time_has_not_been_changed(self.controller.start, end)
            self.fail("Unexpected ok")
        except ValueError:
            self.view.SetStart.assert_called_with(self.controller.start)
            self.view.DisplayInvalidStart.assert_called_with("#You can't change time when the Event is locked#")

    def test_invalid_start(self):
        try:
            self.controller._validate_and_save_start(None)
            self.fail("Unexpected ok")
        except ValueError:
            pass

    def test_invalid_end(self):
        try:
            self.controller._validate_and_save_end(None)
            self.fail("Unexpected ok")
        except ValueError:
            pass

    def test_ends_today(self):
        self.controller.time_type = Mock()
        self.controller.time_type.now.return_value = 0
        self.controller.ends_today = True
        self.controller.start = 1
        try:
            self.controller._validate_ends_today()
            self.fail("Unexpected ok")
        except ValueError:
            self.view.DisplayErrorMessage.assert_called_with("#Start time > Now.#")

    def test_save_to_db(self):
        e = Exception("")
        self.controller.event_repository = Mock()
        self.controller.event_repository.save.side_effect = e
        self.controller.event = Mock()
        self.controller._save_event_to_db()
        self.view.HandleDbError.assert_called_with(e)

    def test_save_container_to_db(self):
        e = Exception("")
        self.controller.event_repository = Mock()
        self.controller.event_repository.save.side_effect = e
        self.controller.container = Mock()
        self.controller._save_container_to_db()
        self.view.HandleDbError.assert_called_with(e)


class describe_save_and_duplicate(EditEventDialogTestCase):

    def test_on_duplicate(self):
        self.when_editing_a_new_event()
        self.simulate_user_clicks_save_and_duplicate()
        self.view.GetDuplicateEventDialog.assert_called_with(self.controller.timeline, self.controller.event)
