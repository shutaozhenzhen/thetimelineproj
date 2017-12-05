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


from timelinelib.wxgui.components.maincanvas.noophandlers.noopbase import NoopBaseHandler
from timelinelib.general.methodcontainer import MethodContainer


class NoopLeftMouseDownOnEvent(NoopBaseHandler):

    def __init__(self, canvas, cursor, keyboard):
        NoopBaseHandler.__init__(self, canvas, cursor, keyboard)

    def run(self, main_frame, state):

        def is_resize_command():
            return self.hit_resize_handle() is not None

        def is_move_command():
            if self.event_at_cursor().get_ends_today():
                return False
            else:
                return self.hit_move_handle()

        def start_event_action(action_method, action_arg):
            if main_frame.ok_to_edit():
                try:
                    action_method(self.event_at_cursor(), action_arg)
                except:
                    main_frame.edit_ends()
                    raise

        def resize_event():
            start_event_action(state.change_to_resize_by_drag, self.hit_resize_handle())

        def move_event():
            start_event_action(state.change_to_move_by_drag, self.time_at_cursor())

        methods = MethodContainer(
            [
                (is_resize_command(), resize_event),
                (is_move_command(), move_event)
            ],
            default_method=self.toggle_event_selection)
        methods.select(True)()
