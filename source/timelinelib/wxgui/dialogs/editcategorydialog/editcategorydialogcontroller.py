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


from timelinelib.data import Category
from timelinelib.db.exceptions import TimelineIOError
from timelinelib.drawing.drawers import get_progress_color
from timelinelib.wxgui.framework import Controller


DEFAULT_COLOR = (255, 0, 0)
DEFAULT_FONT_COLOR = (0, 0, 0)


class EditCategoryDialogController(Controller):

    def on_init(self, category, category_repository):
        self.category = category
        self.category_repository = category_repository
        try:
            tree = self.category_repository.get_tree(remove=self.category)
        except TimelineIOError, e:
            self.view.HandleDbError(e)
        else:
            self.view.SetCategoryTree(tree)
            if self.category is None:
                self.view.SetName("")
                self.view.SetColor(DEFAULT_COLOR)
                self.view.SetProgressColor(get_progress_color(DEFAULT_COLOR))
                self.view.SetDoneColor(get_progress_color(DEFAULT_COLOR))
                self.view.SetFontColor(DEFAULT_FONT_COLOR)
                self.view.SetParent(None)
            else:
                self.view.SetName(self.category.get_name())
                self.view.SetColor(self.category.get_color())
                self.view.SetProgressColor(self.category.get_progress_color())
                self.view.SetDoneColor(self.category.get_done_color())
                self.view.SetFontColor(self.category.get_font_color())
                self.view.SetParent(self.category._get_parent())

    def on_ok_clicked(self, event):
        try:
            new_name = self.view.GetName()
            new_color = self.view.GetColor()
            new_progress_color = self.view.GetProgressColor()
            new_done_color = self.view.GetDoneColor()
            new_font_color = self.view.GetFontColor()
            new_parent = self.view.GetParent()
            if not self._name_valid(new_name):
                self.view.HandleInvalidName(new_name)
                return
            if self._name_in_use(new_name):
                self.view.HandleUsedName(new_name)
                return
            if self.category is None:
                self.category = Category(new_name, new_color, new_font_color,
                                         parent=new_parent)
            else:
                self.category.name = new_name
                self.category.color = new_color
                self.category.progress_color = new_progress_color
                self.category.done_color = new_done_color
                self.category.font_color = new_font_color
                self.category.parent = new_parent
            self.category_repository.save(self.category)
            self.view.EndModalOk()
        except TimelineIOError, e:
            self.view.HandleDbError(e)

    def _name_valid(self, name):
        return len(name) > 0

    def _name_in_use(self, name):
        for cat in self.category_repository.get_all():
            if cat != self.category and cat.get_name() == name:
                return True
        return False
