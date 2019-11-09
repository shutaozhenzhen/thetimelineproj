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


from timelinelib.features.experimental.experimentalfeaturecontainersize import DESCRIPTION
from timelinelib.features.experimental.experimentalfeaturecontainersize import DISPLAY_NAME
from timelinelib.features.experimental.experimentalfeaturecontainersize import CONFIG_NAME
from timelinelib.features.experimental.experimentalfeaturecontainersize import ExperimentalFeatureContainerSize
from timelinelib.test.cases.unit import UnitTestCase


class describe_experimental_feature_done(UnitTestCase):

    def test_has_display_name(self):
        self.assertEqual(DISPLAY_NAME, self.ef.display_name)

    def test_has_config_name(self):
        self.assertEqual(CONFIG_NAME, self.ef.get_config_name())

    def test_has_description(self):
        self.assertEqual(DESCRIPTION, self.ef.description)

    def setUp(self):
        self.ef = ExperimentalFeatureContainerSize()
