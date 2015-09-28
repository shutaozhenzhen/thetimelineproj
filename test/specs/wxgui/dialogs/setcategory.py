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

from timelinelib.calendar.gregorian import GregorianUtils
from timelinelib.data.db import MemoryDB
from timelinelib.data.event import Event
from timelinelib.db import db_open
from timelinelib.time.gregoriantime import GregorianTimeType
from timelinelib.wxgui.dialogs.setcategory.setcategorydialogcontroller import SetCategoryDialogController
from timelinelib.wxgui.dialogs.setcategory.view import SetCategoryDialog
from timelinetest import UnitTestCase
from timelinetest.utils import a_category_with
from timelinetest.utils import create_dialog


class describe_set_category_dialog(UnitTestCase):

    def setUp(self):
        self.view = Mock(SetCategoryDialog)
        self.controller = SetCategoryDialogController(self.view)
        self.time_type = GregorianTimeType()
        self._create_category1()
        self._create_category2()
        self._create_event1()
        self._create_event2()
        self._create_db_mock()
        self.view.GetSelectedCategory.return_value = self.category1

    def _create_db_mock(self):
        def get_all_events():
            return [self.event1, self.event2]
        self.db = Mock(MemoryDB)
        self.db.get_time_type.return_value = self.time_type
        self.db.get_all_events = get_all_events
        return self.db

    def _create_category1(self):
        self.category1 = a_category_with(name="category-name-1")

    def _create_category2(self):
        self.category2 = a_category_with(name="category-name-2")

    def _create_event1(self):
        self.event1 = self._create_event(None)

    def _create_event2(self):
        self.event2 = self._create_event(self.category2)

    def _create_event(self, category):
        return Event(
            self.time_type,
            GregorianUtils.from_date(2010, 1, 1).to_time(),
            GregorianUtils.from_date(2010, 1, 1).to_time(),
            "foo",
            category)

    def test_it_can_be_created(self):
        db = db_open(":tutorial:")
        with create_dialog(SetCategoryDialog, None, db) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()

    def test_category_can_be_set_on_all_events_without_category(self):
        self.controller.on_init(self.db, [])
        self.controller.on_ok_clicked(None)
        self.view.EndModalOk.assert_called_with()
        self.assertEqual(self.event1.get_category(), self.category1)
        self.assertEqual(self.event2.get_category(), self.category2)

    def test_category_can_be_set_when_all_events_has_catageroies(self):
        self.event1.set_category(self.category2)
        self.controller.on_init(self.db, [])
        self.controller.on_ok_clicked(None)
        self.view.EndModalOk.assert_called_with()
        self.assertEqual(self.event1.get_category(), self.category2)
        self.assertEqual(self.event2.get_category(), self.category2)

    def test_displays_error_message_if_no_category_selected(self):
        self.controller.on_init(self.db, [])
        self.view.GetSelectedCategory.return_value = None
        self.controller.on_ok_clicked(None)
        self.view.DisplayErrorMessage.assert_called_with("#You must select a category!#")
