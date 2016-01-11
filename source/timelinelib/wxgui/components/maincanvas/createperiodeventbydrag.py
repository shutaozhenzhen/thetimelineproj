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


from timelinelib.wxgui.components.maincanvas.periodbase import SelectPeriodByDragInputHandler
from timelinelib.wxgui.dialogs.editevent.view import open_create_event_editor


class CreatePeriodEventByDragInputHandler(SelectPeriodByDragInputHandler):

    def __init__(self, state, view, main_frame, config, handle_db_error, initial_time):
        SelectPeriodByDragInputHandler.__init__(self, state, view, main_frame, initial_time)
        self._main_frame = main_frame
        self._config = config
        self._timeline_canvas = view
        self._handle_db_error = handle_db_error

    def end_action(self):
        period = self.get_last_valid_period()
        open_create_event_editor(
            self._main_frame,
            self._config,
            self._timeline_canvas.GetDb(),
            self._handle_db_error,
            period.start_time,
            period.end_time)
