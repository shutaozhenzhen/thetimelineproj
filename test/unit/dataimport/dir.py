# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


import os.path

from timelinelib.dataimport.dir import import_db_from_dir
from timelinelib.dataimport.dir import get_unique_cat_name
from timelinelib.test.cases.unit import UnitTestCase


class describe_import_dir(UnitTestCase):

    def test_can_import_this_dir(self):
        this_dir = os.path.dirname(__file__)
        this_name = os.path.basename(__file__)
        db = import_db_from_dir(this_dir)
        event_names = [event.get_text() for event in db.get_all_events()]
        self.assertTrue(this_name in event_names, "Events: %s" % event_names)


class describe_get_unique_cat_name(UnitTestCase):

    def test_different_dir_names_keeps_cat_names(self):
        used_names = []
        self.assertEquals("temp", get_unique_cat_name("temp", used_names))

    def test_duplicate_dir_names_renames_cat_name(self):
        used_names = ["temp"]
        self.assertEquals("temp(1)", get_unique_cat_name("temp", used_names))

    def test_duplicate_dir_names_renames_cat_names(self):
        used_names = ["temp", "temp(1)"]
        self.assertEquals("temp(2)", get_unique_cat_name("temp", used_names))
