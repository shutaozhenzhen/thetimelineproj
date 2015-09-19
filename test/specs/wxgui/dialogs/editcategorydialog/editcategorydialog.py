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

from timelinelib.data.db import MemoryDB
from timelinelib.db.exceptions import TimelineIOError
from timelinelib.repositories.interface import CategoryRepository
from timelinelib.wxgui.dialogs.editcategorydialog.editcategorydialogcontroller import EditCategoryDialogController
from timelinelib.wxgui.dialogs.editcategorydialog.editcategorydialog import EditCategoryDialog
from timelinetest import UnitTestCase
from timelinetest.utils import a_category_with
from timelinetest.utils import create_dialog


class EditCategoryDialogTestCase(UnitTestCase):

    def setUp(self):
        # Category configuration:
        # foo
        #   foofoo
        # bar
        self.category_repository = Mock(CategoryRepository)
        self.foo = a_category_with(name="foo")
        self.foofoo = a_category_with(name="foofoo", font_color=(0, 255, 0), parent=self.foo)
        self.bar = a_category_with(name="bar")
        self.category_repository.get_all.return_value = [self.foo, self.foofoo, self.bar]
        def get_tree_mock(remove):
            if remove is None:
                return [
                    (self.bar, []),
                    (self.foo, [
                        (self.foofoo,
                            [])
                    ])
                ]
            elif remove is self.foofoo:
                return [
                    (self.bar, []),
                    (self.foo, [])
                ]
            else:
                return []
        self.category_repository.get_tree.side_effect = get_tree_mock
        self.view = Mock(EditCategoryDialog)

    def _initializeControllerWith(self, category):
        self.controller = EditCategoryDialogController(self.view)
        self.controller.on_init(category, self.category_repository)


class describe_edit_category_dialog(UnitTestCase):

    def test_it_can_be_created(self):
        category = None
        db = MemoryDB()
        db.save_category(a_category_with(name="one"))
        db.save_category(a_category_with(name="two"))
        with create_dialog(EditCategoryDialog, None, "title", db, category) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()


class describe_editing_a_new_category(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(None)

    def test_all_categories_in_db_are_listed_as_possible_parents(self):
        self.view.SetCategoryTree.assert_called_with([
            (self.bar, []),
            (self.foo, [
                (self.foofoo, [])
            ])
        ])

    def test_name_is_initialized_to_empty_string(self):
        self.view.SetName.assert_called_with("")

    def test_color_is_initialized_to_red(self):
        self.view.SetColor.assert_called_with((255, 0, 0))

    def test_font_color_is_initialized_to_black(self):
        self.view.SetFontColor.assert_called_with((0, 0, 0))

    def test_parent_is_initialized_to_none(self):
        self.view.SetParent.assert_called_with(None)


class describe_editing_an_existing_category(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(self.foofoo)

    def test_all_categories_in_db_except_the_one_being_edited_are_possible_parents(self):
        self.view.SetCategoryTree.assert_called_with([
            (self.bar, []),
            (self.foo, [])
        ])

    def test_name_is_initialized_from_edited_category(self):
        self.view.SetName.assert_called_with("foofoo")

    def test_color_is_initialixed_from_edited_category(self):
        self.view.SetColor.assert_called_with((255, 0, 0))

    def test_font_color_is_initialixed_from_edited_category(self):
        self.view.SetFontColor.assert_called_with((0, 255, 0))

    def test_parent_is_initialized_from_edited_category(self):
        self.view.SetParent.assert_called_with(self.foo)


class describe_editing_a_category_and_db_raises_exception(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self.category_repository.get_tree.side_effect = TimelineIOError
        self._initializeControllerWith(None)

    def test_error_is_handled_by_view(self):
        self.assertTrue(self.view.HandleDbError.called)

    def test_the_dialog_is_not_closed(self):
        self.assertFalse(self.view.EndModalOk.called)


class describe_saving_a_category(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(None)
        self.view.GetName.return_value = "new_cat"
        self.view.GetColor.return_value = (255, 44, 0)
        self.view.GetFontColor.return_value = (0, 44, 255)
        self.view.GetParent.return_value = self.foo
        self.controller.on_ok_clicked(None)

    def _getSavedCategory(self):
        if not self.category_repository.save.called:
            self.fail("No category was saved.")
        return self.category_repository.save.call_args_list[0][0][0]

    def test_saved_category_has_name_from_view(self):
        self.assertEqual("new_cat", self._getSavedCategory().get_name())

    def test_saved_category_has_color_from_view(self):
        self.assertEqual((255, 44, 0), self._getSavedCategory().get_color())

    def test_saved_category_has_font_color_from_view(self):
        self.assertEqual((0, 44, 255),
                         self._getSavedCategory().get_font_color())

    def test_saved_category_has_parent_from_view(self):
        self.assertEqual(self.foo, self._getSavedCategory()._get_parent())

    def test_the_dialog_is_closed(self):
        self.assertTrue(self.view.EndModalOk.called)


class describe_saving_a_category_but_db_raises_exception(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(None)
        self.view.GetName.return_value = "foobar"
        self.view.GetColor.return_value = (0, 0, 0)
        self.category_repository.save.side_effect = TimelineIOError
        self.controller.on_ok_clicked(None)

    def test_error_is_handled_by_view(self):
        self.assertTrue(self.view.HandleDbError.called)

    def test_the_dialog_is_not_closed(self):
        self.assertFalse(self.view.EndModalOk.called)


class describe_saving_a_category_with_an_invalid_name(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(None)
        self.view.GetName.return_value = ""
        self.controller.on_ok_clicked(None)

    def test_the_category_is_not_saved_to_db(self):
        self.assertFalse(self.category_repository.save.called)

    def test_the_view_shows_an_error_message(self):
        self.assertTrue(self.view.HandleInvalidName.called)

    def test_the_dialog_is_not_closed(self):
        self.assertFalse(self.view.EndModalOk.called)


class describe_saving_a_category_with_a_used_name(EditCategoryDialogTestCase):

    def setUp(self):
        EditCategoryDialogTestCase.setUp(self)
        self._initializeControllerWith(None)
        self.view.GetName.return_value = "foo"
        self.controller.on_ok_clicked(None)

    def test_the_category_is_not_saved_to_db(self):
        self.assertFalse(self.category_repository.save.called)

    def test_the_view_shows_an_error_message(self):
        self.assertTrue(self.view.HandleUsedName.called)

    def test_the_dialog_is_not_closed(self):
        self.assertFalse(self.view.EndModalOk.called)
