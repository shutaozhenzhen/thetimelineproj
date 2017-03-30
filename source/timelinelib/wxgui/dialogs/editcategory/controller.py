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


from timelinelib.canvas.data.exceptions import TimelineIOError
from timelinelib.canvas.data import Category
from timelinelib.canvas.drawing.drawers import get_progress_color
from timelinelib.wxgui.framework import Controller


DEFAULT_COLOR = (255, 0, 0)
DEFAULT_FONT_COLOR = (0, 0, 0)


class EditCategoryDialogController(Controller):

    def get_edited_category(self):
        return self._category

    def on_init(self, category, category_repository):
        self._category = category
        self._category_repository = category_repository
        try:
            self.view.PopulateCategories(exclude=self._category)
        except TimelineIOError as e:
            self.view.HandleDbError(e)
        else:
            if self._category is None:
                self.view.SetName("")
                self.view.SetColor(DEFAULT_COLOR)
                self.view.SetProgressColor(get_progress_color(DEFAULT_COLOR))
                self.view.SetDoneColor(get_progress_color(DEFAULT_COLOR))
                self.view.SetFontColor(DEFAULT_FONT_COLOR)
                self.view.SetParent(None)
            else:
                self.view.SetName(self._category.get_name())
                self.view.SetColor(self._category.get_color())
                self.view.SetProgressColor(self._category.get_progress_color())
                self.view.SetDoneColor(self._category.get_done_color())
                self.view.SetFontColor(self._category.get_font_color())
                self.view.SetParent(self._category._get_parent())

    def on_ok_clicked(self, event):
        if self._category_name_is_valid():
            if self._category is None:
                self._category = Category("", DEFAULT_COLOR, DEFAULT_FONT_COLOR)
            self._update_category_properties()
            self._save()

    def _category_name_is_valid(self):
        new_name = self.view.GetName()
        if not self._is_name_valid(new_name):
            self.view.HandleInvalidName(new_name)
            return False
        if self._is_name_in_use(new_name):
            self.view.HandleUsedName(new_name)
            return False
        return True

    def _update_category_properties(self):
        self._category.name = self.view.GetName()
        self._category.color = self.view.GetColor()
        self._category.progress_color = self.view.GetProgressColor()
        self._category.done_color = self.view.GetDoneColor()
        self._category.font_color = self.view.GetFontColor()
        self._category.parent = self.view.GetParent()

    def _is_name_valid(self, name):
        return len(name) > 0

    def _is_name_in_use(self, name):
        for cat in self._category_repository.get_all():
            if cat != self._category and cat.get_name() == name:
                return True
        return False

    def _save(self):
        try:
            self._category_repository.save(self._category)
        except TimelineIOError as e:
            self.view.HandleDbError(e)
        else:
            self.view.EndModalOk()
