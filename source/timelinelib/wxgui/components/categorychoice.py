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

from timelinelib.data import sort_categories
from timelinelib.db.exceptions import TimelineIOError
from timelinelib.repositories.dbwrapper import DbWrapperCategoryRepository
from timelinelib.wxgui.dialogs.categoryeditors.categorieseditordialog import CategoriesEditor
from timelinelib.wxgui.dialogs.editcategorydialog.editcategorydialog import EditCategoryDialog
import timelinelib.wxgui.utils as gui_utils


class CategoryChoice(wx.Choice):

    def __init__(self, parent, timeline, **kwargs):
        wx.Choice.__init__(self, parent, wx.ID_ANY, **kwargs)
        self.timeline = timeline
        self.category_repository = DbWrapperCategoryRepository(self.timeline)

    def Populate(self, exclude=None, select=None):
        try:
            tree = self.category_repository.get_tree(remove=exclude)
        except:
            self.Clear()
            # We can not do error handling here since this method is also
            # called from the constructor (and then error handling is done by
            # the code calling the constructor).
            raise
        else:
            self._populate_tree(tree)
            self.SetSelectedCategory(select)

    def GetSelectedCategory(self):
        if self.GetSelection() == wx.NOT_FOUND:
            return None
        return self.GetClientData(self.GetSelection())

    def SetSelectedCategory(self, category):
        for index in range(self.GetCount()):
            if self.GetClientData(index) == category:
                self.SetSelection(index)
                return
        self.SetSelection(0)

    def _populate_tree(self, tree):
        self.Clear()
        self.Append("", None)
        self._append_tree(tree)

    def _append_tree(self, tree, indent=""):
        for (category, subtree) in tree:
            self.Append(indent + category.name, category)
            self._append_tree(subtree, indent + "    ")

    def select(self, select_category):
        # We can not do error handling here since this method is also called
        # from the constructor (and then error handling is done by the code
        # calling the constructor).
        self.Clear()
        self.Append("", None) # The None-category
        selection_set = False
        current_item_index = 1
        for cat in sort_categories(self.timeline.get_categories()):
            self.Append(cat.name, cat)
            if cat == select_category:
                self.SetSelection(current_item_index)
                selection_set = True
            current_item_index += 1
        self.last_real_category_index = current_item_index - 1
        self.add_category_item_index = self.last_real_category_index + 2
        self.edit_categoris_item_index = self.last_real_category_index + 3
        self.Append("", None)
        self.Append(_("Add new"), None)
        self.Append(_("Edit categories"), None)
        if not selection_set:
            self.SetSelection(0)
        self.current_category_selection = self.GetSelection()

    def get(self):
        selection = self.GetSelection()
        category = self.GetClientData(selection)
        return category

    def on_choice(self, e):
        new_selection_index = e.GetSelection()
        if new_selection_index > self.last_real_category_index:
            self.SetSelection(self.current_category_selection)
            if new_selection_index == self.add_category_item_index:
                self._add_category()
            elif new_selection_index == self.edit_categoris_item_index:
                self._edit_categories()
        else:
            self.current_category_selection = new_selection_index

    def _add_category(self):
        def create_category_editor():
            return EditCategoryDialog(
                self, _("Add Category"), self.timeline, None)
        def handle_success(dialog):
            if dialog.GetReturnCode() == wx.ID_OK:
                try:
                    self.select(dialog.GetEditedCategory())
                except TimelineIOError, e:
                    gui_utils.handle_db_error_in_dialog(self, e)
        gui_utils.show_modal(create_category_editor,
                             gui_utils.create_dialog_db_error_handler(self),
                             handle_success)

    def _edit_categories(self):
        def create_categories_editor():
            return CategoriesEditor(self, self.timeline)
        def handle_success(dialog):
            try:
                prev_index = self.GetSelection()
                prev_category = self.GetClientData(prev_index)
                self.select(prev_category)
            except TimelineIOError, e:
                gui_utils.handle_db_error_in_dialog(self, e)
        gui_utils.show_modal(create_categories_editor,
                             gui_utils.create_dialog_db_error_handler(self),
                             handle_success)
