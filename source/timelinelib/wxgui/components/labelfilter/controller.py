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


class LabelFilterController:

    def __init__(self, view):
        self._view = view
        self._filter_labels = None
        self._event_labels = None

    def visible(self, event):
        self._filter_labels = self._view.get_labels()
        if not self._filter_labels:
            return True
        event_labels = event.get_data('labels')
        if not event_labels:
            return False
        self._event_labels = event_labels.split()
        if self._view.match_all():
            return self._match_all_filter()
        else:
            return self._match_any_filter()

    def _match_all_filter(self):
        return not [label for label in self._filter_labels if label not in self._event_labels]

    def _match_any_filter(self):
        return [label for label in self._filter_labels if label in self._event_labels]
