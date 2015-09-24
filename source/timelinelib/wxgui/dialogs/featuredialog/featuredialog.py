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

from timelinelib.wxgui.dialogs.featuredialog.featuredialogcontroller import FeatureDialogController
from timelinelib.wxgui.framework import Dialog


class FeatureDialog(Dialog):

    """
    <BoxSizerVertical>
        <StaticText name="feature_text" label="$(feature_text)" width="600" border="ALL" />
        <TextCtrl height="200" style = "TE_MULTILINE|TE_READONLY|TE_RICH|TE_AUTO_URL" border="LEFT|RIGHT|BOTTOM" />
        <DialogButtonsGiveFeatureCloseSizer border="LEFT|RIGHT|BOTTOM"
            event_EVT_BUTTON__ID_GIVE_FEEDBACK="on_give_feature"
        />
    </BoxSizerVertical>
    """

    def __init__(self, parent, feature_text):
        Dialog.__init__(self, FeatureDialogController, parent, {
            "feature_text": feature_text,
        }, title=_("Feedback On Feature"))
        self._make_info_label_bold()
        self.controller.on_init()

    def _make_info_label_bold(self):
        font = self.feature_text.GetFont()
        font.SetWeight(wx.BOLD)
        self.feature_text.SetFont(font)
