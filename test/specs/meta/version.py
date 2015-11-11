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


from timelinetest import UnitTestCase
import timelinelib.meta.version as version


class describe_version_formatting(UnitTestCase):

    def setUp(self):
        self.VERSION = version.VERSION
        self.TYPE = version.TYPE
        self.REVISION_HASH = version.REVISION_HASH
        self.REVISION_DATE = version.REVISION_DATE
        version.VERSION = (1, 2, 3)
        version.TYPE = version.TYPE_BETA
        version.REVISION_HASH = "abc123"
        version.REVISION_DATE = "2015-11-11"

    def tearDown(self):
        version.VERSION = self.VERSION
        version.TYPE = self.TYPE
        version.REVISION_HASH = self.REVISION_HASH
        version.REVISION_DATE = self.REVISION_DATE

    def test_full(self):
        self.assertEqual(
            version.get_version(),
            "1.2.3 beta (abc123 2015-11-11)"
        )

    def test_filename(self):
        self.assertEqual(
            version.get_filename_version(),
            "timeline-1.2.3-beta-abc123-2015-11-11"
        )

    def test_readme(self):
        self.assertEqual(
            version.get_readme_version(),
            "1.2.3 beta"
        )
