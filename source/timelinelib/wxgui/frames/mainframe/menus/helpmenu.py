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
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase
from timelinelib.wxgui.dialogs.feedback.view import show_feedback_dialog
from timelinelib.wxgui.dialogs.systeminfo.view import show_system_info_dialog
from timelinelib.meta.about import display_about_dialog

ID_TUTORIAL = wx.NewId()
ID_NUMTUTORIAL = wx.NewId()
ID_FEEDBACK = wx.NewId()
ID_CONTACT = wx.NewId()
ID_SYSTEM_INFO = wx.NewId()

SHORTCUTS = (wx.ID_HELP, ID_TUTORIAL, ID_FEEDBACK, ID_CONTACT, ID_SYSTEM_INFO)
REQUIRING_TIMELINE = list()


class HelpMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            wx.ID_HELP: parent.help_browser.show_contents_page,
            ID_TUTORIAL: parent.controller.open_gregorian_tutorial_timeline,
            ID_NUMTUTORIAL: parent.controller.open_numeric_tutorial_timeline,
            ID_FEEDBACK: self._feedback,
            ID_CONTACT: parent.help_browser.show_contact_page,
            ID_SYSTEM_INFO: show_system_info_dialog,
            wx.ID_ABOUT: display_about_dialog,
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)

    def create(self):
        menu = self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts(menu)
        self._register_menus_requiring_timeline(menu)
        return menu

    def _create_menu(self):
        menu = wx.Menu()
        menu.Append(wx.ID_HELP, _("&Contents") + "\tF1")
        menu.AppendSeparator()
        menu.Append(ID_TUTORIAL, _("Getting started &tutorial"))
        menu.Append(ID_NUMTUTORIAL, _("Getting started numeric &tutorial"))
        menu.AppendSeparator()
        menu.Append(ID_FEEDBACK, _("Give &Feedback..."))
        menu.Append(ID_CONTACT, _("Co&ntact"))
        menu.AppendSeparator()
        menu.Append(ID_SYSTEM_INFO, _("System information"))
        menu.AppendSeparator()
        menu.Append(wx.ID_ABOUT)
        return menu

    def _feedback(self, evt):
        show_feedback_dialog(parent=None, info="", subject=_("Feedback"), body="")