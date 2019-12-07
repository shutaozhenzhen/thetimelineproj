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


class EventSorter:

    def __init__(self):
        self._sort_order = 0

    def save_sort_order(self, events):
        for event in events:
            if event.is_container():
                self.save_sort_order(event.subevents)
            else:
                if event.sort_order != self._sort_order:
                    event.sort_order = self._sort_order
                    event.save()
                self._sort_order += 1

    @staticmethod
    def length_sort(events):
        reordered_events = [
            event
            for event
            in events
            if not event.is_subevent() and not event.is_milestone()
        ]
        return sorted(reordered_events, key=lambda e: e.length, reverse=True)

