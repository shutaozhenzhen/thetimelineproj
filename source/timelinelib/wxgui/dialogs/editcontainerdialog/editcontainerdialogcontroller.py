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


from timelinelib.data import Container
from timelinelib.repositories.dbwrapper import DbWrapperEventRepository
from timelinelib.wxgui.framework import Controller


class EditContainerDialogController(Controller):

    def on_init(self, db, container):
        self.view.PopulateCategories()
        self._set_initial_values_to_member_variables(db, container)
        self._set_view_initial_values()

    def on_ok_clicked(self, event):
        self.name = self.view.GetName()
        self.category = self.view.GetCategory()
        try:
            self._verify_name()
            if self.container_exists:
                self._update_container()
            else:
                self._create_container()
            self.view.EndModalOk()
        except ValueError:
            pass

    def get_container(self):
        return self.container

    def _set_initial_values_to_member_variables(self, db, container):
        self.db = db
        self.container = container
        self.container_exists = (self.container is not None)
        if self.container_exists:
            self.name = self.container.get_text()
            self.category = self.container.get_category()
        else:
            self.name = ""
            self.category = None

    def _set_view_initial_values(self):
        self.view.SetName(self.name)
        self.view.SetCategory(self.category)

    def _verify_name(self):
        name_is_invalid = (self.name == "")
        if name_is_invalid:
            msg = _("Field '%s' can't be empty.") % _("Name")
            self.view.DisplayInvalidName(msg)
            raise ValueError()

    def _update_container(self):
        self.container.update_properties(self.name, self.category)
        self._save_to_db()

    def _save_to_db(self):
        try:
            DbWrapperEventRepository(self.db).save(self.container)
            raise Exception()
        except Exception, ex:
            self.view.DisplayDbException(ex)
            raise ex

    def _create_container(self):
        time_type = self.db.get_time_type()
        start = time_type.now()
        end = start
        self.container = Container(time_type, start, end, self.name,
                                   self.category)
