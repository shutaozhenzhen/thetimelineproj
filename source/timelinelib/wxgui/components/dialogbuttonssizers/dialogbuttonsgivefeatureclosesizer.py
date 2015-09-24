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


import wx

from timelinelib.wxgui.components.dialogbuttonssizers.dialogbuttonssizer import DialogButtonsSizer


class DialogButtonsGiveFeatureCloseSizer(DialogButtonsSizer):

    def __init__(self, parent):
        self.parent = parent
        DialogButtonsSizer.__init__(self, parent)
        parent.btn_give_feature = wx.Button(parent, wx.ID_ANY, _("Give Feature"))
        parent.btn_close = wx.Button(parent, wx.ID_CLOSE)
        self.buttons = (parent.btn_give_feature, parent.btn_close)
        self.default = len(self.buttons) - 1
        self.AddButtons()
        parent.SetEscapeId(wx.ID_ANY)
        parent.SetAffirmativeId(wx.ID_CLOSE)

    def AddButtons(self):
        self.Add(self.parent.btn_give_feature, 0, wx.LEFT | wx.EXPAND)
        self.AddStretchSpacer()
        self.Add(self.parent.btn_close, 0, wx.LEFT | wx.EXPAND)
