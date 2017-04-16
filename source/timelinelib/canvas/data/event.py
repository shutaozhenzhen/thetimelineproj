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


from timelinelib.canvas.drawing.drawers import get_progress_color
from timelinelib.canvas.data.item import TimelineItem


DEFAULT_COLOR = (200, 200, 200)
EXPORTABLE_FIELDS = (_("Text"), _("Description"), _("Start"), _("End"), _("Category"),
                     _("Fuzzy"), _("Locked"), _("Ends Today"), _("Hyperlink"),
                     _("Progress"), _("Progress Color"), _("Done Color"), _("Alert"),
                     _("Is Container"), _("Is Subevent"))


class Event(TimelineItem):

    def __init__(self, start_time, end_time, text, category=None,
                 fuzzy=False, locked=False, ends_today=False):
        self.fuzzy = fuzzy
        self.locked = locked
        self.ends_today = ends_today
        self.id = None
        self.update(start_time, end_time, text, category)
        self._milestone = False
        self._highlighted = False
        self._highlight_count = 0
        self.data = {}

    def __eq__(self, other):
        return (isinstance(other, Event) and
                self.get_fuzzy() == other.get_fuzzy() and
                self.get_locked() == other.get_locked() and
                self.get_ends_today() == other.get_ends_today() and
                self.get_id() == other.get_id() and
                self.get_time_period() == other.get_time_period() and
                self.get_text() == other.get_text() and
                self.get_category() == other.get_category() and
                self.get_description() == other.get_description() and
                self.get_hyperlink() == other.get_hyperlink() and
                self.get_progress() == other.get_progress() and
                self.get_alert() == other.get_alert() and
                self.get_icon() == other.get_icon() and
                self.get_default_color() == other.get_default_color())

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        raise NotImplementedError("I don't believe this is in use.")

    def __gt__(self, other):
        raise NotImplementedError("I don't believe this is in use.")

    def __le__(self, other):
        raise NotImplementedError("I don't believe this is in use.")

    def __ge__(self, other):
        raise NotImplementedError("I don't believe this is in use.")

    def __repr__(self):
        return "Event<id=%r, text=%r, time_period=%r, ...>" % (
            self.get_id(), self.get_text(), self.get_time_period())

    def get_id(self):
        return self.id

    def has_id(self):
        return self.id is not None

    def set_id(self, event_id):
        self.id = event_id
        return self

    def set_end_time(self, time):
        self.set_time_period(self.get_time_period().set_end_time(time))

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text.strip()
        return self

    def get_category(self):
        return self.category

    def get_category_name(self):
        if self.get_category():
            return self.get_category().get_name()
        else:
            return None

    def set_category(self, category):
        self.category = category
        return self

    def get_fuzzy(self):
        return self.fuzzy

    def set_fuzzy(self, fuzzy):
        self.fuzzy = fuzzy
        return self

    def get_locked(self):
        return self.locked

    def set_locked(self, locked):
        self.locked = locked
        return self

    def get_ends_today(self):
        return self.ends_today

    def set_ends_today(self, ends_today):
        if not self.locked:
            self.ends_today = ends_today
        return self

    def get_description(self):
        return self.get_data("description")

    def set_description(self, description):
        self.set_data("description", description)
        return self

    def get_icon(self):
        return self.get_data("icon")

    def set_icon(self, icon):
        self.set_data("icon", icon)
        return self

    def get_hyperlink(self):
        return self.get_data("hyperlink")

    def set_hyperlink(self, hyperlink):
        self.set_data("hyperlink", hyperlink)
        return self

    def get_alert(self):
        return self.get_data("alert")

    def set_alert(self, alert):
        self.set_data("alert", alert)
        return self

    def get_progress(self):
        return self.get_data("progress")

    def set_progress(self, progress):
        self.set_data("progress", progress)
        return self

    def get_default_color(self):
        color = self.get_data("default_color")
        if color is None:
            color = DEFAULT_COLOR
        return color

    def set_default_color(self, color):
        self.set_data("default_color", color)
        return self

    def get_done_color(self):
        if self.category:
            return self.category.get_done_color()
        else:
            return get_progress_color(DEFAULT_COLOR)

    def get_progress_color(self):
        category = self.category
        if category:
            if self.get_progress() == 100:
                return category.get_done_color()
            else:
                return category.get_progress_color()
        else:
            return get_progress_color(DEFAULT_COLOR)

    def update(self, start_time, end_time, text, category=None, fuzzy=None,
               locked=None, ends_today=None):
        """Change the event data."""
        self.update_period(start_time, end_time)
        self.text = text.strip()
        self.category = category
        if ends_today is not None:
            if not self.locked:
                self.ends_today = ends_today
        if fuzzy is not None:
            self.fuzzy = fuzzy
        if locked is not None:
            self.locked = locked

    def get_data(self, event_id):
        """
        Return data with the given id or None if no data with that id exists.

        See set_data for information how ids map to data.
        """
        return self.data.get(event_id, None)

    def set_data(self, event_id, data):
        """
        Set data with the given id.

        Here is how ids map to data:

            description - string
            icon - wx.Bitmap
        """
        self.data[event_id] = data

    def has_data(self):
        """Return True if the event has associated data, or False if not."""
        for event_id in self.data:
            if self.data[event_id] is not None:
                return True
        return False

    def has_balloon_data(self):
        """Return True if the event has associated data to be displayed in a balloon."""
        return (self.get_data("description") is not None or
                self.get_data("icon") is not None)

    def get_label(self, time_type):
        """Returns a unicode label describing the event."""
        event_label = u"%s (%s)" % (
            self.text,
            time_type.format_period(self.get_time_period()),
        )
        duration_label = self._get_duration_label(time_type)
        if duration_label != "":
            return u"%s  %s: %s" % (event_label, _("Duration"), duration_label)
        else:
            return event_label

    def _get_duration_label(self, time_type):
        label = time_type.format_delta(self.time_span())
        if label == "0":
            label = ""
        return label

    def clone(self):
        # Objects of type datetime are immutable.
        new_event = Event(
            self.get_start_time(),
            self.get_end_time(),
            self.text,
            self.category
        )
        # Description is immutable
        new_event.set_data("description", self.get_data("description"))
        # Icon is immutable in the sense that it is never changed by our
        # application.
        new_event.set_data("icon", self.get_data("icon"))
        new_event.set_data("hyperlink", self.get_data("hyperlink"))
        new_event.set_data("progress", self.get_data("progress"))
        new_event.set_data("alert", self.get_data("alert"))
        new_event.set_data("default_color", self.get_data("default_color"))
        new_event.set_fuzzy(self.get_fuzzy())
        new_event.set_ends_today(self.get_ends_today())
        new_event.set_locked(self.get_locked())
        return new_event

    def is_container(self):
        return False

    def is_subevent(self):
        return False

    def is_milestone(self):
        return False

    def get_exportable_fields(self):
        return EXPORTABLE_FIELDS

    def set_milestone(self, value):
        self._milestone = value

    def get_milestone(self):
        return self._milestone

    def highlight(self, value):
        self._highlighted = value
        self._highlight_count = 0

    def is_highlighted(self):
        return self._highlighted

    def get_highlight_count(self):
        return self._highlight_count

    def increment_highlight_count(self):
        self._highlight_count += 1


def clone_event_list(eventlist):
    from timelinelib.canvas.data.container import Container
    from timelinelib.canvas.data.subevent import Subevent

    def clone_events():
        events = []
        for event in eventlist:
            new_event = event.clone()
            new_event.set_id(event.get_id())
            events.append(new_event)
        return events

    def get_containers(cloned_events):
        containers = {}
        for event in cloned_events:
            if isinstance(event, Container):
                containers[event.container_id] = event
        return containers

    def get_subevents(cloned_events):
        subevents = []
        for event in cloned_events:
            if isinstance(event, Subevent):
                subevents.append(event)
        return subevents

    def update_container_subevent_relations(containers, subevents):
        for subevent in subevents:
            try:
                subevent.container = containers[subevent.container_id]
                subevent.container.events.append(subevent)
            except:
                pass
    eventlist = clone_events()
    containers = get_containers(eventlist)
    subevents = get_subevents(eventlist)
    update_container_subevent_relations(containers, subevents)
    return eventlist
