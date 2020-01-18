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


from timelinelib.canvas.data import TimePeriod
from timelinelib.wxgui.framework import Controller


class PeriodPickerController(Controller):

    def get_value(self):
        return TimePeriod(self._get_start(), self._get_end())

    def set_value(self, time_period):
        self.view.SetStartValue(time_period.get_start_time())
        self.view.SetEndValue(time_period.get_end_time())
        self.view.SetShowPeriod(time_period.is_period())
        self.view.SetShowTime(time_period.has_nonzero_time())

    def on_period_checkbox_changed(self, event):
        self.view.SetShowPeriod(event.IsChecked())

    def on_show_time_checkbox_changed(self, event):
        self.view.SetShowTime(event.IsChecked())

    def _get_start(self):
        return self.view.GetStartValue()

    def _get_end(self):
        if self.view.GetShowPeriod():
            return self.view.GetEndValue()
        else:
            return self._get_start()
