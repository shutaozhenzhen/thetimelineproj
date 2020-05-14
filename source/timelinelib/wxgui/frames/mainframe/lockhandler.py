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


import getpass
import os

from timelinelib.wxgui.utils import display_warning_message


class LockedException(Exception):
    pass


class LockHandler:

    def __init__(self, main_frame):
        self._main_frame = main_frame
        self._path = None
        self._pid = None

    def locked(self, path):
        self._path = path
        return os.path.exists(self._get_lockpath())

    def the_lock_is_mine(self, path):
        self._path = path
        try:
            with open(self._get_lockpath(), "r") as fp:
                lines = fp.readlines()
            lines = [line.strip() for line in lines]
            return lines[0] == getpass.getuser() and lines[2] == f"{os.getpid()}"
        except:
            return False

    def lock(self, path, timeline):
        self._path = path
        if not timeline.get_should_lock():
            return
        try:
            ts = timeline.get_timestamp_string()
            self._pid = os.getpid()
            with open(self._get_lockpath(), "w") as fp:
                fp.write(f"{getpass.getuser()}\n{ts}\n{self._pid}")
        except Exception:
            msg = _(
                "Unable to take lock on %s\nThis means you can't edit the timeline.\nCheck if you have write access to this directory.") % self._timelinepath
            display_warning_message(msg, self._main_frame)
            raise LockedException()

    def unlock(self, path):
        self._path = path
        lockpath = self._get_lockpath()
        if os.path.exists(lockpath):
            try:
                os.remove(lockpath)
                self._path = None
            except WindowsError as ex:
                if ex.winerror == 32:
                    self._report_other_process_uses_lockfile(lockpath)
                else:
                    raise ex

    def _get_lockpath(self):
        return f"{self._path}.lock"

    def _report_other_process_uses_lockfile(self, lockpath):
        message = _(f"""The lockfile used to protect the timeline from concurrent updates is opened by another program or process.
    This lockfile must be removed in order be able to continue editing the timeline!
    The lockfile is found at: {lockpath}""")
        display_warning_message(message, self._main_frame)
