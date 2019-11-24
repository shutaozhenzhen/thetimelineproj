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


from timelinelib.wxgui.framework import Controller
from timelinelib.proxies.sidebar import SidebarProxy


class MilestoneFinderDialogController(Controller):

    def on_init(self, db, mainframe):
        self._db = db
        self._mainframe = mainframe
        self.view.SetMilestones(self._get_milestone_names())

    def on_ok(self, evt):
        canvas = self._mainframe.main_panel.get_timeline_canvas()
        event = self._get_milestone_by_text()
        canvas.Navigate(lambda tp: tp.center(event.mean_time()))
        canvas.HighligtEvent(event, clear=True)
        self.view.EndModalOk()

    def on_doubble_click(self, evt):
        self.on_ok(evt)

    def _get_milestone_names(self):
        return sorted([milestone.text for milestone in self._db.all_milestones])

    def _get_milestone_by_text(self):
        text = self.view.GetMilestone()
        return [milestone for milestone in self._db.all_milestones if milestone.text == text][0]
