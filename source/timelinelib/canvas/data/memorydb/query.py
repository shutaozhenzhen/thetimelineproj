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


from timelinelib.canvas.data import Category
from timelinelib.canvas.data import Container
from timelinelib.canvas.data import Era
from timelinelib.canvas.data import Event
from timelinelib.canvas.data import Milestone
from timelinelib.canvas.data import Subevent


class Query:

    def __init__(self, db, immutable_db):
        self._db = db
        self._immutable_db = immutable_db
        self._wrappers = {}

    def container_exists(self, id_):
        return id_ in self._immutable_db.containers

    def event_exists(self, id_):
        return id_ in self._immutable_db.events

    def milestone_exists(self, id_):
        return id_ in self._immutable_db.milestones

    def get_category(self, id_):
        if id_ not in self._wrappers:
            self._wrappers[id_] = self._create_category_wrapper(id_)
        return self._wrappers[id_]

    def get_container(self, id_):
        if id_ not in self._wrappers:
            self._wrappers[id_] = self._create_container_wrapper(id_)
            self._load_subevents(self._wrappers[id_])
        return self._wrappers[id_]

    def get_event(self, id_):
        if id_ not in self._wrappers:
            self._wrappers[id_] = self._create_event_wrapper(id_)
            immutable_event = self._immutable_db.events.get(id_)
            if immutable_event.container_id is not None:
                # Loading the container will load and populate all subevents
                self.get_container(immutable_event.container_id)
        return self._wrappers[id_]

    def get_milestone(self, id_):
        if id_ not in self._wrappers:
            self._wrappers[id_] = self._create_milestone_wrapper(id_)
        return self._wrappers[id_]

    def get_era(self, id_):
        if id_ not in self._wrappers:
            self._wrappers[id_] = self._create_era_wrapper(id_)
        return self._wrappers[id_]

    def _load_subevents(self, container):
        for subevent_id, immutable_event in self._immutable_db.events:
            if immutable_event.container_id == container.id:
                self.get_event(subevent_id).container = container

    def _create_category_wrapper(self, id_):
        immutable_category = self._immutable_db.categories.get(id_)
        wrapper = Category(
            db=self._db,
            id_=id_,
            immutable_value=immutable_category,
        )
        wrapper.parent = self._get_maybe_category(immutable_category.parent_id)
        return wrapper

    def _create_container_wrapper(self, id_):
        immutable_container = self._immutable_db.containers.get(id_)
        wrapper = Container(
            db=self._db,
            id_=id_,
            immutable_value=immutable_container,
        )
        wrapper.category = self._get_maybe_category(immutable_container.category_id)
        lst = []
        for key in immutable_container.category_ids:
            lst.append(self._get_maybe_category(key))
        wrapper.set_categories(lst)
        return wrapper

    def _create_event_wrapper(self, id_):
        immutable_event = self._immutable_db.events.get(id_)
        if immutable_event.container_id is None:
            klass = Event
        else:
            klass = Subevent
        wrapper = klass(
            db=self._db,
            id_=id_,
            immutable_value=immutable_event,
        )
        wrapper.category = self._get_maybe_category(immutable_event.category_id)
        lst = []
        for key in immutable_event.category_ids:
            lst.append(self._get_maybe_category(key))
        wrapper.set_categories(lst)
        return wrapper

    def _create_milestone_wrapper(self, id_):
        immutable_milestone = self._immutable_db.milestones.get(id_)
        wrapper = Milestone(
            db=self._db,
            id_=id_,
            immutable_value=immutable_milestone,
        )
        wrapper.category = self._get_maybe_category(immutable_milestone.category_id)
        lst = []
        for key in immutable_milestone.category_ids:
            lst.append(self._get_maybe_category(key))
        wrapper.set_categories(lst)
        return wrapper

    def _create_era_wrapper(self, id_):
        immutable_era = self._immutable_db.eras.get(id_)
        return Era(
            db=self._db,
            id_=id_,
            immutable_value=immutable_era,
        )

    def _get_maybe_category(self, category_id):
        if category_id is None:
            return None
        else:
            return self.get_category(category_id)
