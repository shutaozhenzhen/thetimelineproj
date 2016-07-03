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


from timelinelib.wxgui.framework import Controller
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data.milestone import Milestone


class EditMilestoneDialogController(Controller):

    def on_init(self, db, milestone):
        self._db = db
        self._time_type = db.time_type
        if milestone is None:
            self._new_milestone = True
            self._milestone = Milestone(db, self._time_type.now(), "")
        else:
            self._new_milestone = False
            self._milestone = milestone
        self.view.PopulateControls(self._milestone.time_period.start_time, self._milestone.get_text(),
                                   self._milestone.get_default_color())

    def on_ok_clicked(self, evt):
        self._update_milestone()
        self.view.Close()

    def show_time_checkbox_on_checked(self, evt):
        pass

    def _update_milestone(self):
        self._milestone.set_description(self.view.GetDescription())
        self._milestone.set_text("milestone")
        self._milestone.set_default_color(self.view.GetColour()[:3])
        self._milestone.set_time_period(TimePeriod(self._time_type, self.view.GetTime(), self.view.GetTime()))
        if self._new_milestone:
            self._save_milestone_to_db()

    def _save_milestone_to_db(self):
        try:
            self._db.save_event(self._milestone)
        except Exception, e:
            self.view.HandleDbError(e)

    def get_milestone(self):
        return self._milestone