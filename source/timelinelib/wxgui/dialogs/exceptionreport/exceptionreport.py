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

import sys
import traceback

import wx

from timelinelib.wxgui.dialogs.textdisplay.view import TextDisplayDialog


def exception_report(main_frame, message):
    query = _("Show more details?")
    res = main_frame.DisplayErrorMessage(message + "\n\n" + query, yesno=True)
    if res == wx.ID_YES:
        dlg = TextDisplayDialog(_('Error information'))
        type_, value_, traceback_ = sys.exc_info()
        info = traceback.format_exception(type_, value_, traceback_)
        dlg.SetText(''.join(info))
        dlg.ShowModal()
