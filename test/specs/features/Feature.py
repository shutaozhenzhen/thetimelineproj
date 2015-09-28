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


from mock import Mock

from timelinelib.features.feature import Feature
from timelinelib.features.installed.installedfeatures import InstalledFeatures
from timelinelib.wxgui.dialogs.feature.featuredialog import FeatureDialog
from timelinelib.wxgui.dialogs.feature.featuredialog import FeatureDialogController
from timelinetest import UnitTestCase


DISPLAY_NAME = "Display name"
DESCRIPTION = "Display description"


class FeedbackFormSpec(UnitTestCase):

    def test_shows_parts_in_dialog(self):
        self.dialog.SetFeatureName.assert_called_with(self.key.get_display_name())
        self.dialog.SetFeatureDescription.assert_called_with(self.key.get_description())

    def setUp(self):
        self.key = InstalledFeatures().get_all_features()[0]
        self.dialog = Mock(FeatureDialog)
        self.controller = FeatureDialogController(self.dialog)
        self.controller.on_init(self.key)


class describe_feature(UnitTestCase):

    def test_has_a_display_name(self):
        self.assertEqual(DISPLAY_NAME, self.feature.get_display_name())

    def test_has_a_description(self):
        self.assertEqual(DESCRIPTION, self.feature.get_description())

    def setUp(self):
        self.feature = Feature(DISPLAY_NAME, DESCRIPTION)
