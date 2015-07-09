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


import time
import wx

from timelinelib.wxgui.dialogs.eraeditor import EraEditorDialog
from timelinelib.data.era import Era


class ErasEditorController(object):

    def __init__(self, view, timeline, config):
        self.view = view
        self.eras = timeline.get_all_eras()
        self.eras.sort()
        self.timeline = timeline
        self.time_type = self.timeline.get_time_type()
        self.config = config
        view.populate(self.eras)

    def edit(self, era):
        dlg = EraEditorDialog(self.view, _("Edit an Era"), self.time_type, self.config, era)
        if dlg.ShowModal() == wx.ID_OK:
            self.view.update(era)
        dlg.Destroy()

    def delete(self, era):
        if era in self.eras:
            self.eras.remove(era)
            self.view.remove(era)

    def add(self):
        era = self._create_era()
        dlg = EraEditorDialog(self.view, _("Add an Era"), self.time_type, self.config, era)
        if dlg.ShowModal() == wx.ID_OK:
            self.eras.append(era)
            self.view.append(era)
            self.timeline.save_era(era)
        dlg.Destroy()

    def _create_era(self):
        if self.time_type.is_date_time_type():
            start = self.time_type.parse_time("%s 00:00:00" % time.strftime("%Y-%m-%d"))
        else:
            start = self.time_type.now()
        end = start
        return Era(self.time_type, start, end, "New Era")
