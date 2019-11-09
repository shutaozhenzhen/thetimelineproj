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
from unittest.mock import Mock

from timelinelib.wxgui.dialogs.feature.controller import FeatureDialogController
from timelinelib.wxgui.dialogs.feature.view import FeatureDialog
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.features.installed.installedfeatures import InstalledFeatures


DISPLAY_NAME = "Feature display name"
FEATURE_DESCRIPTION = "Feature description"


class describe_feature_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(FeatureDialog)
        self.controller = FeatureDialogController(self.view)
        self.feature = Mock()
        self.feature.display_name = DISPLAY_NAME
        self.feature.get_description.return_value = FEATURE_DESCRIPTION

    def test_view_is_populated_when_controller_inits(self):
        self.controller.on_init(self.feature)
        self.view.SetFeatureName.assert_called_with(DISPLAY_NAME)
        self.view.SetFeatureDescription.assert_called_with(FEATURE_DESCRIPTION)

    def test_can_extract_url_from_event(self):
        evt = Mock(wx.TextUrlEvent)
        evt.GetURLStart.return_value = 2
        evt.GetURLEnd.return_value = 19
        self.view.GetDescription.return_value = "  http://www.xxx.se  "
        self.assertEqual("http://www.xxx.se", self.controller._get_url(evt))


class describe_feature_dialog_controller_(UnitTestCase):

    def test_shows_parts_in_dialog(self):
        self.dialog.SetFeatureName.assert_called_with(self.key.display_name)
        self.dialog.SetFeatureDescription.assert_called_with(self.key.get_description())

    def setUp(self):
        self.key = InstalledFeatures().get_all_features()[0]
        self.dialog = Mock(FeatureDialog)
        self.controller = FeatureDialogController(self.dialog)
        self.controller.on_init(self.key)
