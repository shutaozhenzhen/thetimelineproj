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
import timelinelib.wxgui.frames.mainframe.menus as mid
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.wxgui.dialogs.feedback.view import show_feedback_dialog
from timelinelib.wxgui.dialogs.systeminfo.view import show_system_info_dialog
from timelinelib.meta.about import display_about_dialog
from timelinelib.wxgui.frames.helpbrowserframe.helpbrowserframe import HelpBrowserFrame

SHORTCUTS = (mid.ID_HELP, mid.ID_TUTORIAL, mid.ID_FEEDBACK, mid.ID_CONTACT, mid.ID_SYSTEM_INFO)
REQUIRING_TIMELINE = list()


class HelpMenu(MenuBase):

    def __init__(self, parent):
        help_browser = HelpBrowserFrame(parent)
        event_handlers = {
            mid.ID_HELP: help_browser.show_contents_page,
            mid.ID_TUTORIAL: parent.controller.open_gregorian_tutorial_timeline,
            mid.ID_NUMTUTORIAL: parent.controller.open_numeric_tutorial_timeline,
            mid.ID_FEEDBACK: lambda evt: show_feedback_dialog(parent=None, info="", subject=_("Feedback"), body=""),
            mid.ID_CONTACT: help_browser.show_contact_page,
            mid.ID_SYSTEM_INFO: show_system_info_dialog,
            mid.ID_ABOUT: display_about_dialog,
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)
        self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts()
        self._register_menus_requiring_timeline()

    def _create_menu(self):
        self.Append(mid.ID_HELP, _("&Contents") + "\tF1")
        self.AppendSeparator()
        self.Append(mid.ID_TUTORIAL, _("Getting started &tutorial"))
        self.Append(mid.ID_NUMTUTORIAL, _("Getting started numeric &tutorial"))
        self.AppendSeparator()
        self.Append(mid.ID_FEEDBACK, _("Give &Feedback..."))
        self.Append(mid.ID_CONTACT, _("Co&ntact"))
        self.AppendSeparator()
        self.Append(mid.ID_SYSTEM_INFO, _("System information"))
        self.AppendSeparator()
        self.Append(mid.ID_ABOUT)
