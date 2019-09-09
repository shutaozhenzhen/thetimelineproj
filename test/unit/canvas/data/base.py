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


from unittest.mock import Mock

from timelinelib.canvas.data.base import ItemBase
from timelinelib.test.cases.unit import UnitTestCase


class describe_new_item_base(UnitTestCase):

    def test_can_set_db(self):
        mock_db = Mock()
        another_mock_db = Mock()
        category = ItemBase(None, None, None)
        self.assertTrue(category.db is None)
        category.db = mock_db
        self.assertTrue(category.db is mock_db)
        category.db = mock_db
        self.assertTrue(category.db is mock_db)
        with self.assertRaises(Exception):
            category.db = another_mock_db
