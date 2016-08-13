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
from timelinelib.canvas.data.milestone import MILESTONE_TEXT


class EditMilestoneDialogController(Controller):

    def on_init(self, db, milestone):
        self._db = db
        self._time_type = db.time_type
        if milestone is None:
            self._new_milestone = True
            self._milestone = Milestone(db, self._time_type.now(), "")
            self._milestone.set_description("")
        else:
            self._new_milestone = False
            self._milestone = milestone
        self._populate_view()

    def _populate_view(self):
        self.view.SetTime(self._milestone.time_period.start_time)
        self.view.SetColor(self._milestone.get_default_color())
        self.view.SetDescription(self._milestone.get_description())
        self.view.SetShowTime(self._milestone_has_nonzero_time())
        label = self._milestone.get_text()
        try:
            label = label.split(":")[1]
        except:
            label = ""
        self.view.SetLable(label)
        self.view.SetCategory(self._milestone.get_category())

    def _milestone_has_nonzero_time(self):
        return self._time_type.time_period_has_nonzero_time(self._milestone.get_time_period())

    def on_ok_clicked(self, evt):
        self._update_milestone()
        self.view.Close()

    def show_time_checkbox_on_checked(self, evt):
        self.view.SetShowTime(evt.IsChecked())

    def _update_milestone(self):
        if self.view.GetDescription() == "":
            self._milestone.set_description(None)
        else:
            self._milestone.set_description(self.view.GetDescription())
        self._milestone.set_text(MILESTONE_TEXT + "%s" % self.view.GetLabel())
        self._milestone.set_default_color(self.view.GetColour()[:3])
        self._milestone.set_time_period(TimePeriod(self._time_type, self.view.GetTime(), self.view.GetTime()))
        self._milestone.set_category(self.view.GetCategory())
        if self._new_milestone:
            self._save_milestone_to_db()

    def _save_milestone_to_db(self):
        try:
            self._db.save_event(self._milestone)
        except Exception, e:
            self.view.HandleDbError(e)

    def get_milestone(self):
        return self._milestone
