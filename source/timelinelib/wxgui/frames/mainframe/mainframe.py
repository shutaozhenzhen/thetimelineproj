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


import wx
import wx.lib.newevent

from timelinelib.canvas.data import TimePeriod
from timelinelib.config.dotfile import read_config
from timelinelib.config.wxlocale import set_wx_locale
from timelinelib.db import db_open
from timelinelib.features.experimental.experimentalfeatures import ExperimentalFeatures
from timelinelib.meta.about import APPLICATION_NAME
from timelinelib.wxgui.frames.mainframe.mainframecontroller import LockedException
from timelinelib.wxgui.frames.mainframe.mainframecontroller import MainFrameController
from timelinelib.wxgui.utils import display_error_message
import timelinelib.wxgui.frames.mainframe.guicreator as guic
from timelinelib.wxgui.frames.mainframe.alertcontroller import AlertController
from timelinelib.wxgui.frames.mainframe.menucontroller import MenuController
from timelinelib.wxgui.dialogs.duplicateevent.view import open_duplicate_event_dialog_for_event
from timelinelib.db.utils import safe_locking
from timelinelib.wxgui.dialogs.setcategory.view import open_set_category_dialog
from timelinelib.wxgui.dialogs.eraseditor.view import oped_edit_eras_dialog
from timelinelib.wxgui.utils import load_icon_bundle
from timelinelib.wxgui.dialogs.timeeditor.view import open_time_editor_dialog
from timelinelib.wxgui.dialogs.changenowdate.view import open_change_now_date_dialog


CatsViewChangedEvent, EVT_CATS_VIEW_CHANGED = wx.lib.newevent.NewCommandEvent()


def skip_when_no_event_selected(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except IndexError:
            pass
    return wrapper


class MainFrame(wx.Frame, guic.GuiCreator):

    def __init__(self, application_arguments):
        self.config = read_config(application_arguments.get_config_file_path())
        wx.Frame.__init__(self, None, size=self.config.get_window_size(),
                          pos=self.config.get_window_pos(),
                          style=wx.DEFAULT_FRAME_STYLE, name="main_frame")
        self.Bind(EVT_CATS_VIEW_CHANGED, self._on_cats_view_changed)
        self.Bind(wx.EVT_CLOSE, self.exit)
        self.locale = set_wx_locale()
        # self.help_browser = HelpBrowserFrame(self)
        self.controller = MainFrameController(self, db_open, self.config)
        self.menu_controller = MenuController()
        self.timeline = None
        ExperimentalFeatures().set_active_state_on_all_features_from_config_string(
            self.config.experimental_features)
        self._create_gui()
        self.Maximize(self.config.window_maximized)
        self.SetTitle(APPLICATION_NAME)
        self.SetIcons(load_icon_bundle())
        self.main_panel.show_welcome_panel()
        self.EnableDisableMenus()
        self.controller.on_started(application_arguments)
        self._alert_controller = AlertController(self).start_timer()
        self.prev_time_period = None

    def DisplayErrorMessage(self, message):
        """This function is hard to remove due to tests using it."""
        display_error_message(message, parent=self)

    def DisplayStatus(self, message):
        self.status_bar_adapter.set_text(message)

    def DisplayReadonly(self, text):
        self.status_bar_adapter.set_read_only_text(text)

    @property
    def canvas(self):
        return self.main_panel.canvas

    @property
    def view_properties(self):
        return self.canvas.GetViewProperties()

    # Concurrent editing
    def ok_to_edit(self):
        try:
            return self.controller.ok_to_edit()
        except LockedException:
            return False

    def edit_ends(self):
        self.controller.edit_ends()

    # General menu functions
    def EnableDisableMenus(self):
        """Also used by TimelinePanel."""
        self.menu_controller.update_menus_enabled_state(self.timeline, self.main_panel)

    # File Menu action handlers (New, Open, Open recent, Save as, Import, Export, Exit
    def create_new_timeline(self, timetype=None):
        self.controller.create_new_timeline(timetype)

    def open_existing_timeline(self):
        self.controller.open_existing_timeline()

    def open_recent_timeline(self, event):
        path = self.open_recent_map[event.GetId()]
        self.controller.open_timeline_if_exists(path)

    def save_as(self):
        self.controller.save_as()

    def exit(self, event):
        self._alert_controller.stop_timer()
        self._save_application_config()
        try:
            if self.ok_to_edit():
                self.save_current_timeline_data()
        finally:
            self.edit_ends()
        self.Destroy()

    def update_open_recent_submenu(self):
        self._clear_recent_menu_items()
        self._create_recent_menu_items()

    def _clear_recent_menu_items(self):
        for item in self.mnu_file_open_recent_submenu.GetMenuItems():
            self.mnu_file_open_recent_submenu.Delete(item)

    def display_timeline(self, timeline):
        self.timeline = timeline
        self.menu_controller.on_timeline_change(timeline)
        self.main_panel.display_timeline(timeline)
        self.controller.set_title()
        self.DisplayReadonly(self.controller.get_readonly_text_in_status_bar())

    def get_visible_categories(self):
        if self.config.filtered_listbox_export:
            return [cat for cat in self.timeline.get_categories()
                    if self.view_properties.is_category_visible(cat)]
        else:
            return [cat for cat in self.timeline.get_categories()]

    def get_export_periods(self):
        return self.main_panel.get_export_periods(*self._get_start_and_end_for_all_visible_events())

    @property
    def file_open_recent_submenu(self):
        return self.mnu_file_open_recent_submenu

    def _save_application_config(self):
        self.config.set_window_size(self.GetSize())
        self.config.set_window_pos(self.GetPosition())
        self.config.window_maximized = self.IsMaximized()
        self.config.sidebar_width = self.main_panel.get_sidebar_width()
        self.config.write()

    def save_current_timeline_data(self):
        if self.timeline:
            self.main_panel.save_view_properties(self.timeline)

    # View menu action handlers
    def start_slide_show(self):
        self.controller.start_slide_show()

    # Timeline menu action handlers
    @skip_when_no_event_selected
    def edit_event(self):
        self.main_panel.open_event_editor(self._get_first_selected_event())

    @skip_when_no_event_selected
    def duplicate_event(self):
        open_duplicate_event_dialog_for_event(self, self, self.timeline, self._get_first_selected_event())

    @skip_when_no_event_selected
    def set_category_on_selected(self):
        event = self._get_first_selected_event() # Ensure that at least one event is selected
        safe_locking(self, lambda: self._set_category_to_selected_events())

    def _set_category_to_selected_events(self):
        open_set_category_dialog(self, self.timeline, self.main_panel.get_selected_event_ids())

    def measure_distance_between_events(self):
        self.controller.measure_distance_between_events(self.main_panel.get_ids_of_two_first_selected_events())

    def set_category(self):
        open_set_category_dialog(self, self.timeline)

    def edit_eras(self):
        oped_edit_eras_dialog(self, self.timeline, self.config)

    def set_timeline_in_readonly_mode(self):
        self.timeline.set_readonly()
        self.DisplayReadonly(self.controller.get_readonly_text_in_status_bar())
        self.EnableDisableMenus()

    # Navigation menu event handlers
    def update_navigation_menu_items(self):
        self._clear_navigation_menu_items()
        if self.timeline:
            self._create_navigation_menu_items()
            self.shortcut_controller.add_navigation_functions()

    def fit_all_events(self):
        self.main_panel.FitAllEvents(self._period_for_all_visible_events())

    def restore_time_period(self):
        if self.prev_time_period:
            self.main_panel.Navigate(lambda tp: self.prev_time_period)

    def navigate_to_first_event(self):
        self.main_panel.navigate_to_first_event(self.timeline.get_first_event())

    def navigate_to_last_event(self):
        self.main_panel.navigate_to_last_event(
            self.timeline.get_last_event(),
            self.timeline.get_time_type().get_min_time())

    def display_time_editor_dialog(self, time_type, initial_time, handle_new_time_fn, title):
        open_time_editor_dialog(self, self.config, time_type, initial_time, handle_new_time_fn, title)

    def display_now_date_editor_dialog(self, handle_new_time_fn, title):
        open_change_now_date_dialog(self, self.config, self.timeline, handle_new_time_fn, title)

    def save_time_period(self):
        self.prev_time_period = self.main_panel.get_time_period()

    # Helper functions for finding events
    def _get_first_selected_event(self):
        return self.timeline.find_event_with_id(self.main_panel.get_id_of_first_selected_event())

    def _period_for_all_visible_events(self):
        return TimePeriod(*self._get_start_and_end_for_all_visible_events()).zoom(-1)

    def _get_start_and_end_for_all_visible_events(self):
        return self.timeline.get_start_and_end_for_all_visible_events(self.view_properties.filter_events)

    # Event handlers
    def _on_cats_view_changed(self, evt):
        self.main_panel.get_view_properties().change_view_cats_individually(evt.is_checked)

    # Config functions
    def week_starts_on_monday(self):
        return self.config.get_week_start() == "monday"
