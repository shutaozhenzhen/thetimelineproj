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


from mock import Mock
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.cursor import Cursor
from timelinelib.wxgui.keyboard import Keyboard
from timelinelib.wxgui.components.maincanvas.noop import NoOpInputHandler
from timelinelib.wxgui.components.maincanvas.noophandlers.mousemoved import NoopMouseMoved
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedown import NoopLeftMouseDown
from timelinelib.wxgui.components.maincanvas.noophandlers.leftmousedclick import NoopLeftMouseDclick


class describe_noop_mouse_move(UnitTestCase):

    def test_deleagte_is_called(self):
        delegate = Mock(NoopMouseMoved)
        status_bar = Mock()
        handler = NoOpInputHandler(None,
                                   status_bar,
                                   None,
                                   None,
                                   delegates=lambda key, canvas, cursor, keyboard: delegate)
        handler.mouse_moved(10, 10, False)
        delegate.run.assert_called_with(status_bar)


class describe_left_mouse_down(UnitTestCase):

    def test_deleagte_is_called(self):
        delegate = Mock(NoopLeftMouseDown)
        main_frame = Mock()
        state = Mock()
        handler = NoOpInputHandler(state,
                                   None,
                                   main_frame,
                                   None,
                                   delegates=lambda key, canvas, cursor, keyboard: delegate)
        handler.left_mouse_down(0, 0, False, False, False)
        delegate.run.assert_called_with(main_frame, state)


class describe_left_dclick(UnitTestCase):

    def test_deleagte_is_called(self):
        delegate = Mock(NoopLeftMouseDclick)
        handler = NoOpInputHandler(None,
                                   None,
                                   None,
                                   None,
                                   delegates=lambda key, canvas, cursor, keyboard: delegate)
        handler.left_mouse_dclick(Cursor(0, 0), Keyboard(False, False, False))
        delegate.run.assert_called_with()
