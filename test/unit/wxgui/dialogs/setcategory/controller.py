# -*- coding: utf-8 -*-
#
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

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import an_event_with
from timelinelib.wxgui.dialogs.setcategory.controller import SetCategoryDialogController
from timelinelib.wxgui.dialogs.setcategory.view import SetCategoryDialog


class describe_set_category_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(SetCategoryDialog)
        self.controller = SetCategoryDialogController(self.view)
        self.db = MemoryDB()
        self._create_category1()
        self._create_category2()
        self._create_event1()
        self._create_event2()
        self.view.GetSelectedCategory.return_value = self.category1

    def _create_category1(self):
        self.category1 = a_category_with(name="category-1")
        self.db.save_category(self.category1)

    def _create_category2(self):
        self.category2 = a_category_with(name="category-2")
        self.db.save_category(self.category2)

    def _create_event1(self):
        self.event1 = self._create_event("event-1", None)
        self.db.save_event(self.event1)

    def _create_event2(self):
        self.event2 = self._create_event("event-2", self.category2)
        self.db.save_event(self.event2)

    def _create_event(self, text, category):
        return an_event_with(
            time="1 Jan 2010",
            text=text,
            category=category
        )

    def assertEventsHaveCategories(self, events_categories):
        self.assertEqual({
            event.text: event.category.name if event.category else None
            for event
            in self.db.get_all_events()
        }, {
            event.text: category.name if category else None
            for event, category
            in events_categories
        })

    def test_category_can_be_set_on_all_events_without_category(self):
        self.view.GetSelectedCategory.return_value = self.category2
        self.controller.on_init(self.db, [])
        self.controller.on_ok_clicked(None)
        self.view.EndModalOk.assert_called_with()
        self.assertEventsHaveCategories([
            (self.event1, self.category2),
            (self.event2, self.category2),
        ])

    def test_category_can_be_set_on_selected_events(self):
        self.view.GetSelectedCategory.return_value = self.category1
        self.controller.on_init(self.db, [self.event1.id])
        self.controller.on_ok_clicked(None)
        self.view.EndModalOk.assert_called_with()
        self.assertEventsHaveCategories([
            (self.event1, self.category1),
            (self.event2, self.category2),
        ])

    def test_category_can_be_set_when_all_events_have_catageroies(self):
        self.event1.set_category(self.category2)
        self.event1.save()
        self.controller.on_init(self.db, [])
        self.controller.on_ok_clicked(None)
        self.view.EndModalOk.assert_called_with()
        self.assertEventsHaveCategories([
            (self.event1, self.category2),
            (self.event2, self.category2),
        ])

    def test_displays_error_message_if_no_category_selected(self):
        self.controller.on_init(self.db, [])
        self.view.GetSelectedCategory.return_value = None
        self.controller.on_ok_clicked(None)
        self.view.DisplayErrorMessage.assert_called_with(
            u"⟪You must select a category!⟫"
        )

    def test_title_set_for_no_selected_events(self):
        self.controller.on_init(self.db, [])
        self.view.SetTitle.assert_called_with(
            u"⟪Set Category on events without category⟫"
        )

    def test_title_set_for_selected_events(self):
        self.controller.on_init(self.db, [self.event1.id])
        self.view.SetTitle.assert_called_with(
            u"⟪Set Category on selected events⟫"
        )
