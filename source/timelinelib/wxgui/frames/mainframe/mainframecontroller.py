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


import os

from timelinelib.wxgui.dialogs.getfilepath.view import open_get_file_path_dialog, FUNC_SAVE_AS, FUNC_OPEN, FUNC_NEW
from timelinelib.db.utils import get_new_path_from_user
from timelinelib.wxgui.dialogs.slideshow.view import open_slideshow_dialog
from timelinelib.wxgui.utils import display_error_message
from timelinelib.wxgui.utils import display_warning_message
from timelinelib.wxgui.utils import get_user_ack
from timelinelib.dataexport.timelinexml import export_db_to_timeline_xml
from timelinelib.wxgui.utils import display_information_message
from timelinelib.wxgui.frames.mainframe.lockhandler import LockHandler, LockedException
from timelinelib.meta.about import get_title
from timelinelib.wxgui.dialogs.exceptionreport.exceptionreport import exception_report
from timelinelib.db.utils import get_modification_date


class MainFrameController:

    def __init__(self, main_frame, db_open_fn, config):
        self._main_frame = main_frame
        self._db_open_fn = db_open_fn
        self._config = config
        self._timeline = None
        self._timelinepath = None
        self._last_changed = None
        self._lock_handler = LockHandler(main_frame)
        self._error_dialog = display_error_message

    def on_started(self, application_arguments):
        if application_arguments.has_files():
            self._open_or_create_timeline(application_arguments.get_first_file())
        elif self._config.has_recently_opened_files():
            self.open_timeline_if_exists(self._config.get_latest_recently_opened_file())

    def set_error_dialog(self, error_dialog):
        """For test purposes."""
        self._error_dialog = error_dialog

    def open_timeline_if_exists(self, path):
        if os.path.exists(path):
            self._open_or_create_timeline(path)
        else:
            display_error_message(_("File '%s' does not exist.") % path, self._main_frame)

    # GUI updates
    def set_title(self):
        self._main_frame.SetTitle(get_title(self._timelinepath))

    def get_readonly_text_in_status_bar(self):
        if self._timeline is not None and self._timeline.is_read_only():
            return _("read-only")
        return ""

    # Concurrent editing
    def ok_to_edit(self):
        if self._timeline is None:
            return True
        if self._timeline.is_read_only():
            return False
        if self._lock_handler.locked(self._timelinepath):
            display_warning_message("The Timeline is Locked by someone else.\nTry again later")
            return False
        if not os.path.exists(self._timelinepath):
            self._lock_handler.lock(self._timelinepath, self._timeline)
            return True
        last_changed = get_modification_date(self._timelinepath)
        if last_changed > self._last_changed:
            ack = get_user_ack(
                _("Someone else has changed the Timeline.\nYou have two choices!\n  1. Set Timeline in Read-Only mode.\n  2. Synchronize Timeline.\n\nDo you want to Synchronize?"))
            if ack:
                self._reload_from_disk()
            else:
                self._main_frame.set_timeline_in_readonly_mode()
            return False
        if last_changed > 0:
            self._lock_handler.lock(self._timelinepath, self._timeline)
        return True

    def edit_ends(self):
        if self._lock_handler.the_lock_is_mine(self._timelinepath):
            self._last_changed = get_modification_date(self._timelinepath)
            self._lock_handler.unlock(self._timelinepath)

    # File Menu action handlers (New, Open, Open recent, Save as, Import, Export, Exit
    def create_new_timeline(self, timetype):
        path = get_new_path_from_user(timetype, self._timelinepath)
        self._open_or_create_timeline(path, timetype)

    def open_existing_timeline(self):
        path = ""
        if self._timeline is not None:
            path = os.path.dirname(self._timeline.path)
        self._open_or_create_timeline(open_get_file_path_dialog(FUNC_OPEN, path))

    def save_as(self):
        path = open_get_file_path_dialog(FUNC_SAVE_AS, self._timeline.path)
        self._main_frame.save_current_timeline_data()
        if path is not None:
            assert path.endswith(".timeline")
            export_db_to_timeline_xml(self._timeline, path)
            self._open_or_create_timeline(path, save_current_data=False)

    # View menu action handlers
    def start_slide_show(self):
        open_slideshow_dialog(self._timeline, self._main_frame.canvas)

    # Timeline menu action handlers
    def measure_distance_between_events(self, event_ids):
        caption = _("Distance between selected events")
        display_information_message(caption, self._timeline.get_distance_info(event_ids))

    # Help menu action handlers
    def open_gregorian_tutorial_timeline(self, *args, **kwargs):
        self._open_or_create_timeline(":tutorial:")

    def open_numeric_tutorial_timeline(self, *args, **kwargs):
        self._open_or_create_timeline(":numtutorial:")

    # Internal functions
    def _open_or_create_timeline(self, path, timetype=None, save_current_data=True):
        if path is not None:
            if save_current_data:
                self._main_frame.save_current_timeline_data()
            try:
                self._timeline = self._db_open_fn(path, timetype=timetype)
            except Exception as e:
                message = _("Unable to open timeline '%s'.") % path + "\n\n" + str(e)
                exception_report(self._error_dialog, message)
            else:
                self._config.append_recently_opened(path)
                self._main_frame.update_open_recent_submenu()
                self._timelinepath = self._timeline.path = path
                self._main_frame.display_timeline(self._timeline)
                self._last_changed = get_modification_date(self._timelinepath)
                self._main_frame.update_navigation_menu_items()
                self._main_frame.EnableDisableMenus()

    def _reload_from_disk(self):
        self._open_or_create_timeline(self._timelinepath, save_current_data=False)
        self._main_frame.canvas.Redraw()
