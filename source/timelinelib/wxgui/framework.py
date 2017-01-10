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


from humblewx import Controller
from humblewx import SMALL_BORDER
import humblewx
import wx

from timelinelib.wxgui.utils import display_error_message
from timelinelib.wxgui.utils import display_information_message
from timelinelib.wxgui.utils import handle_db_error_by_crashing
from timelinelib.wxgui.utils import _set_focus_and_select


class HandleDbErrorMixin(object):

    def HandleDbError(self, e):
        assert isinstance(self, wx.Window)
        handle_db_error_by_crashing(e, self)


class Dialog(humblewx.Dialog, HandleDbErrorMixin):

    def EndModalOk(self):
        self.EndModal(wx.ID_OK)

    def DisplayErrorMessage(self, message, focus_widget=None):
        display_error_message(message, parent=self)
        if focus_widget is not None:
            _set_focus_and_select(focus_widget)

    def DisplayInformationMessage(self, caption, message):
        display_information_message(caption, message, parent=self)
