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
from unittest.mock import sentinel

from timelinelib.calendar.num.timetype import NumTimeType
from timelinelib.canvas.data.container import Container
from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data.subevent import Subevent
from timelinelib.config.dotfile import Config
from timelinelib.repositories.interface import EventRepository
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event
from timelinelib.test.utils import an_event_with
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.test.utils import ObjectWithTruthValue
from timelinelib.wxgui.dialogs.editevent.controller import EditEventDialogController
from timelinelib.wxgui.dialogs.editevent.view import EditEventDialog


class EditEventDialogControllerTestCase(UnitTestCase):

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
            self.db.time_type,
            self.event_repository,
            self.db,
            start,
            end,
            event)
        self.view.GetContainer.return_value = None
        self.view.IsAddMoreChecked.return_value = False
        if start is not None and end is not None:
            self.view.GetPeriod.return_value = TimePeriod(start, end)

    def when_editor_opened_with_num(self, start, end, event):
        self.controller.on_init(
            self.config,
            NumTimeType(),
            self.event_repository,
            self.num_db,
            start,
            end,
            event)

    def simulate_user_enters_period(self, start, end):
        self.view.GetPeriod.return_value = gregorian_period(start, end)

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

    def simulate_container_changed(self):
        evt = Mock()
        self.controller.on_container_changed(evt)

    def simulate_user_selects_a_container(self, subevent):
        time_period = subevent.get_time_period()
        container = Container().update(
            time_period.start_time,
            time_period.start_time,
            "container"
        )
        container.register_subevent(subevent)
        self.view.GetContainer.return_value = container
        return container

    def simulate_user_clicks_enlarge_button(self, enlarged=True):
        with self.wxapp():
            evt = Mock()
            if enlarged:
                self.controller.reduced_size = sentinel.REDUCE_SIZE
                self.controller.reduced_pos = sentinel.REDUCE_POS
                self.controller.on_reduce_click(evt)
            else:
                self.controller.on_enlarge_click(evt)

    def get_saved_event(self):
        self.assertEqual(len(self.event_repository.save.call_args_list), 1)
        return self.event_repository.save.call_args_list[0][0][0]

    def assert_start_time_set_to(self, time):
        self.view.SetStart.assert_called_with(human_time_to_gregorian(time))

    def assert_end_time_set_to(self, time):
        self.view.SetEnd.assert_called_with(human_time_to_gregorian(time))

    def assert_no_event_saved(self):
        self.assertFalse(self.event_repository.save.called)
        self.assertFalse(self.view.EndModal.called)
        self.assertFalse(self.view.ClearEventData.called)


class describe_period_field(EditEventDialogControllerTestCase):

    def test_has_value_from_first_argument_if_only_one_given(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.SetPeriod.assert_called_with(
            gregorian_period("1 Jan 2010", "1 Jan 2010")
        )

    def test_has_value_from_second_argument(self):
        self.when_editor_opened_with_period("1 Jan 2010", "2 Jan 2010")
        self.view.SetPeriod.assert_called_with(
            gregorian_period("1 Jan 2010", "2 Jan 2010")
        )

    def test_has_value_from_event(self):
        self.when_editor_opened_with_event(an_event_with(
            human_start_time="1 Jan 2010",
            human_end_time="2 Jan 2010"
        ))
        self.view.SetPeriod.assert_called_with(
            gregorian_period("1 Jan 2010", "2 Jan 2010")
        )


class describe_period_field_period(EditEventDialogControllerTestCase):

    def test_is_shown_if_shown_previous_time(self):
        self.config.event_editor_show_period = True
        self.when_editor_opened_with_event(None)
        self.view.SetShowPeriod.assert_called_with(True)

    def test_is_hidden_if_hidden_previous_time(self):
        self.config.event_editor_show_period = False
        self.when_editor_opened_with_event(None)
        self.view.SetShowPeriod.assert_called_with(False)


class describe_period_field_time(EditEventDialogControllerTestCase):

    def test_is_shown_if_shown_previous_time(self):
        self.config.event_editor_show_time = True
        self.when_editor_opened_with_event(None)
        self.view.SetShowTime.assert_called_with(True)

    def test_is_hidden_if_hidden_previous_time(self):
        self.config.event_editor_show_time = False
        self.when_editor_opened_with_event(None)
        self.view.SetShowTime.assert_called_with(False)


class describe_fuzzy_checkbox(EditEventDialogControllerTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetFuzzy.assert_called_with(False)

    def test_has_value_from_event(self):
        event = an_event()
        event.set_fuzzy(sentinel.FUZZY)
        self.when_editor_opened_with_event(event)
        self.view.SetFuzzy.assert_called_with(sentinel.FUZZY)


class describe_locked_checkbox(EditEventDialogControllerTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetLocked.assert_called_with(False)

    def test_has_value_from_event(self):
        event = an_event_with(locked=sentinel.LOCKED)
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


class describe_start_is_in_history(EditEventDialogControllerTestCase):

    def test_new_event_starting_in_history(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.assertTrue(self.controller._start_is_in_history())

    def test_event_not_starting_in_history(self):
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 3010"))
        self.assertFalse(self.controller._start_is_in_history())

    def test_event_starting_in_history(self):
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))
        self.assertTrue(self.controller._start_is_in_history())


class describe_ends_today_checkbox(EditEventDialogControllerTestCase):

    def test_is_not_checked_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetEndsToday.assert_called_with(False)

    def test_has_value_from_event(self):
        event = an_event()
        event.set_ends_today(sentinel.ENDS_TODYAY)
        self.when_editor_opened_with_event(event)
        self.view.SetEndsToday.assert_called_with(sentinel.ENDS_TODYAY)

    def test_no_endtime_check(self):
        self.when_editor_opened_with_period("2 Jan 2010", "3 Jan 2010")
        self.view.GetEndsToday.return_value = True
        self.simulate_user_clicks_ok()
        self.assertGreater(
            self.get_saved_event().get_end_time(),
            human_time_to_gregorian("3 Jan 2010")
        )


class describe_text_field(EditEventDialogControllerTestCase):

    def test_has_no_value_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetName.assert_called_with("")

    def test_has_value_from_event(self):
        event = an_event()
        event.set_text("hello")
        self.when_editor_opened_with_event(event)
        self.view.SetName.assert_called_with("hello")


class describe_category_field(EditEventDialogControllerTestCase):

    def test_has_no_value_by_default(self):
        self.when_editing_a_new_event()
        self.view.SetCategory.assert_called_with(None)

    def test_has_value_from_event(self):
        event = an_event()
        event.set_category(sentinel.CATEGORY)
        self.when_editor_opened_with_event(event)
        self.view.SetCategory.assert_called_with(sentinel.CATEGORY)


class describe_additional_data(EditEventDialogControllerTestCase):

    def test_is_populated_from_event(self):
        event = an_event()
        event.data = {"description": "hello"}
        self.when_editor_opened_with_event(event)
        self.view.SetEventData.assert_called_with({
            "description": "hello",
            "icon": None,
            "hyperlink": None,
            "alert": None,
            "progress": None,
            "default_color": None,
        })

    def test_is_not_set_for_new_events(self):
        self.when_editing_a_new_event()
        self.assertFalse(self.view.SetEventData.called)


class describe_add_more_checkbox(EditEventDialogControllerTestCase):

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
        self.view.GetPeriod.return_value = gregorian_period(
            "1 Jan 2010", "2 Jan 2010"
        )
        self.view.GetFuzzy.return_value = sentinel.FUZZY
        self.view.GetLocked.return_value = self.locked_value
        self.view.GetEndsToday.return_value = self.ends_today_value
        self.view.GetName.return_value = "new event"
        self.view.GetCategory.return_value = sentinel.CATEGORY
        self.view.GetEventData.return_value = {}
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
        self.assertEqual(self.saved_event.data, {
            "description": None,
            "icon": None,
            "hyperlink": None,
            "alert": None,
            "progress": None,
            "default_color": None,
        })


class describe_saving_new(EditEventDialogControllerTestCase, describe_saving):

    def setUp(self):
        EditEventDialogControllerTestCase.setUp(self)
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


class describe_saving_existing(EditEventDialogControllerTestCase, describe_saving):

    def setUp(self):
        EditEventDialogControllerTestCase.setUp(self)
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))


class describe_validation(EditEventDialogControllerTestCase):

    def test_period_must_be_valid(self):
        self.when_editing_a_new_event()
        self.view.GetPeriod.side_effect = ValueError
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidPeriod.called)
        self.assert_no_event_saved()

    def test_period_can_be_long(self):
        self.when_editor_opened_with_time("1 Jan 2010")
        self.view.GetName.return_value = "a valid name"  # why needed?
        self.view.GetLocked.return_value = False  # why needed?
        self.view.GetEndsToday.return_value = False
        self.simulate_user_enters_period("1 Jan 2000", "1 Jan 5000")
        self.simulate_user_clicks_ok()
        self.assertEqual(0, self.view.DisplayErrorMessage.call_count)

    def test_time_cant_change_when_event_is_locked(self):
        self.when_editor_opened_with_event(an_event_with(time="1 Jan 2010"))
        self.simulate_user_enters_period("1 Jan 2011 12:00", "2 Jan 2011 12:00")
        self.view.GetLocked.return_value = True
        self.simulate_user_clicks_ok()
        self.view.DisplayInvalidPeriod.assert_called_with(
            _("You can't change time when the Event is locked"))
        self.assert_no_event_saved()


class describe_ends_today_in_container(EditEventDialogControllerTestCase):

    def test_set_ends_today_on_subevent_extends_container_period(self):
        start = human_time_to_gregorian("1 Jan 2010")
        today = human_time_to_gregorian("1 Jan 2015")
        subevent = Subevent().update(start, start, "subevent")
        self.when_editor_opened_with_event(subevent)
        container = self.simulate_user_selects_a_container(subevent)
        self.db.time_type.now = lambda: today
        self.view.GetEndsToday.return_value = True
        self.simulate_user_enters_period("1 Jan 2010", "1 Jan 2010")
        self.view.GetLocked.return_value = False
        self.controller._update_event()
        self.assertTrue(container.get_time_period().ends_at(today))

    def test_container_allows_ends_today(self):
        self.view.GetContainer.return_value = None
        self.assertTrue(self.controller._container_allows_ends_today())

    def test_update_event_delete(self):
        self.when_editing_a_new_event()
        self.view.GetContainer.return_value = Mock()
        self.controller.event = Mock()
        self.controller.timeline = Mock()
        self.controller.timeline.get_containers.return_value = []
        self.controller.event.is_subevent.return_value = False
        self.view.GetLocked.return_value = False
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
        self.view.GetLocked.return_value = False
        self.controller._update_event()
        self.controller.container.register_subevent.asert_called_with(self.controller.event)

    def test_update_event_(self):
        self.when_editing_a_new_event()
        self.controller.container = None
        self.controller.event = Mock()
        self.controller.timeline = Mock()
        self.controller.event.is_subevent.return_value = True
        self.view.GetLocked.return_value = False
        self.controller._update_event()
        self.assertEqual(1, self.controller.timeline.delete_event.call_count)


class describe_enlarging(EditEventDialogControllerTestCase):

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


class describe_changing_container(EditEventDialogControllerTestCase):

    def test(self):
        self.when_editing_a_new_event()
        self.simulate_container_changed()
        self.assertEqual(1, self.view.EnableEndsToday.call_count)
        self.assertEqual(1, self.view.EnableLocked.call_count)


class describe_exceptions(EditEventDialogControllerTestCase):

    def test_start_changed(self):
        event = an_event_with(
            human_start_time="10 Jan 2010",
            human_end_time="20 Jan 2010"
        )
        self.when_editor_opened_with_event(event)
        self.view.GetLocked.return_value = True
        self.view.GetEndsToday.return_value = False
        self.simulate_user_enters_period("1 Jan 2010", "20 Jan 2010")
        self.simulate_user_clicks_ok()
        self.view.SetPeriod.assert_called_with(
            gregorian_period("10 Jan 2010", "20 Jan 2010")
        )
        self.view.DisplayInvalidPeriod.assert_called_with(
            "⟪You can't change time when the Event is locked⟫"
        )

    def test_end_changed(self):
        event = an_event_with(
            human_start_time="10 Jan 2010",
            human_end_time="20 Jan 2010"
        )
        self.when_editor_opened_with_event(event)
        self.view.GetLocked.return_value = True
        self.view.GetEndsToday.return_value = False
        self.simulate_user_enters_period("10 Jan 2010", "30 Jan 2010")
        self.simulate_user_clicks_ok()
        self.view.SetPeriod.assert_called_with(
            gregorian_period("10 Jan 2010", "20 Jan 2010")
        )
        self.view.DisplayInvalidPeriod.assert_called_with(
            "⟪You can't change time when the Event is locked⟫"
        )

    def test_invalid_period(self):
        self.when_editing_a_new_event()
        self.view.GetPeriod.side_effect = ValueError
        self.simulate_user_clicks_ok()
        self.assertTrue(self.view.DisplayInvalidPeriod.called)

    def test_ends_today(self):
        self.when_editor_opened_with_event(an_event())
        self.db.time_type.now = lambda: human_time_to_gregorian("1 Jan 2010")
        self.view.GetEndsToday.return_value = True
        self.view.GetLocked.return_value = False
        self.simulate_user_enters_period("10 Jan 2010", "20 Jan 2010")
        self.simulate_user_clicks_ok()
        self.view.DisplayInvalidPeriod.assert_called_with(
            "⟪End must be > Start⟫"
        )


class describe_save_and_duplicate(EditEventDialogControllerTestCase):

    def test_on_duplicate(self):
        self.when_editing_a_new_event()
        self.simulate_user_clicks_save_and_duplicate()
        self.view.GetDuplicateEventDialog.assert_called_with(self.controller.timeline, self.controller.event)
