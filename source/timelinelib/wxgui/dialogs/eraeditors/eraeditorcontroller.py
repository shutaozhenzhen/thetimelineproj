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


from timelinelib.data import TimePeriod
from timelinelib.data import PeriodTooLongError
from timelinelib.time.gregoriantime import GregorianTimeType


class EraEditorDialogApi(object):
    """
    This class defines the API used by the dialog.
    """

    def on_btn_ok(self):
        try:
            self._validate_input()
            self._update_era()
            self.view.close()
        except ValueError:
            pass


class EraEditorDialogController(EraEditorDialogApi):
    """
    This class is the dialog controller.

    It populates the dialog at startup and it validates the
    entered data before it closes the dialog.
    """

    def __init__(self, view, era, time_type=GregorianTimeType()):
        EraEditorDialogApi.__init__(self)
        self.view = view
        self.era = era
        self.time_type = time_type
        self._populate_view()

    def _populate_view(self):
        self.view.set_start(self.era.get_time_period().start_time)
        self.view.set_end(self.era.get_time_period().end_time)
        self.view.set_name(self.era.get_name())
        self.view.set_color(self.era.get_color())
        self.view.set_show_time(self._era_has_nonzero_time())
        self.view.set_focus_on("start")

    def _era_has_nonzero_time(self):
        try:
            return self.era.get_time_period().has_nonzero_time()
        except Exception:
            return False

    def _validate_input(self):
        self._validate_name()
        self._validate_start()
        self._validate_end()
        self._validate_period()
        self._validate_period_length()
        self._validate_color()

    def _validate_name(self):
        name = self.view.get_name()
        if name == "":
            msg = _("Field '%s' can't be empty.") % _("Name")
            self.view.display_invalid_name(msg)
            raise ValueError()

    def _validate_start(self):
        try:
            self.view.get_start()
        except ValueError:
            msg = _("Invalid start time.")
            self.view.display_invalid_start(msg)
            raise

    def _validate_end(self):
        try:
            self.view.get_end()
        except ValueError:
            msg = _("Invalid end time.")
            self.view.display_invalid_end(msg)
            raise

    def _validate_period(self):
            start = self.view.get_start()
            end = self.view.get_end()
            if start > end:
                msg = _("End must be > Start")
                self.view.display_invalid_start(msg)
                raise ValueError()

    def _validate_period_length(self):
        try:
            start = self.view.get_start()
            end = self.view.get_end()
            TimePeriod(self.time_type, start, end)
        except PeriodTooLongError:
            self.view.display_invalid_period(_("Entered period is too long."))
            raise ValueError()

    def _validate_color(self):
        color = self.view.get_color()[:3]
        if min(color) < 0 or max(color) > 255:
            msg = _("Invalid color value")
            self.view.display_invalid_color(msg)
            raise ValueError()

    def _update_era(self):
        w = self.view
        self.era.update(w.get_start(), w.get_end(), w.get_name(), w.get_color()[:3])
