# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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

from timelinelib.wxgui.dialogs.eraeditor import EraEditorDialog
from timelinelib.data.era import Era


class ErasEditorController(object):

    def __init__(self, view, eras, timeline, config):
        self.view = view
        self.eras = eras
        self.eras.sort()
        self.timeline = timeline
        self.time_type = self.timeline.get_time_type()
        self.config = config
        view.populate_listbox(self.eras)

    def edit(self, era):
        dlg = EraEditorDialog(self.view, _("Edit an Era"), self.time_type, self.config, era)
        if dlg.ShowModal() == wx.ID_OK:
            self.view.update(era)
        dlg.Destroy()

    def delete(self, era):
        if era in self.eras:
            self.eras.remove(era)
            return True
        return False

    def add(self):
        era = Era(self.time_type, self.time_type.now(), self.time_type.now(), "New Era")
        dlg = EraEditorDialog(self.view, _("Add an Era"), self.time_type, self.config, era)
        if dlg.ShowModal() == wx.ID_OK:
            self.eras.append(era)
            self.view.append(era)
            self.timeline.save_era(era)
        dlg.Destroy()
