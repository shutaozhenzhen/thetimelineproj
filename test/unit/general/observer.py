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


from mock import Mock

from timelinelib.general.observer import Listener
from timelinelib.general.observer import Observable
from timelinelib.test.cases.unit import UnitTestCase


class describe_observable(UnitTestCase):

    def test_at_construction_there_area_zero_observers(self):
        self.assertTrue(len(self.observable._observers) == 0)

    def test_an_observer_can_be_registered(self):
        self.registerObserver()
        self.assertTrue(len(self.observable._observers) == 1)

    def test_an_observer_can_be_unregistered(self):
        self.registerObserver()
        self.observable.unregister(self.observer.event_triggered)
        self.assertTrue(len(self.observable._observers) == 0)

    def test_an_observer_gets_notifications(self):
        self.registerObserver()
        self.observable._notify("bar")
        self.observable._notify("foo")
        self.assertTrue(len(self.observer.events) == 2)
        self.assertTrue(self.observer.events[0] == "bar")
        self.assertTrue(self.observer.events[1] == "foo")

    def test_can_listen_for_specific_events(self):
        observer = Observer()
        self.observable.listen_for("bananas", observer.event_triggered2)
        self.observable._notify("apples")
        self.observable._notify("bananas")
        self.assertEqual(len(observer.events), 1)

    def test_can_listen_for_all_events(self):
        observer = Observer()
        self.observable.listen_for_any(observer.event_triggered2)
        self.observable._notify()
        self.observable._notify()
        self.assertEqual(len(observer.events), 2)

    def test_can_unlisten(self):
        observer = Observer()
        self.observable.listen_for_any(observer.event_triggered2)
        self.observable._notify()
        self.observable.unlisten(observer.event_triggered2)
        self.observable._notify()
        self.assertEqual(len(observer.events), 1)

    def setUp(self):
        self.observable = Observable()

    def registerObserver(self):
        self.observer = Observer()
        self.observable.register(self.observer.event_triggered)


class describe_listener(UnitTestCase):

    def test_does_not_call_callback_at_construction(self):
        Listener(self.callback)
        self.assertFalse(self.callback.called)

    def test_calls_callback_when_observable_set(self):
        Listener(self.callback).set_observable(self.observable)
        self.callback.assert_called_with(self.observable)

    def test_calls_callback_when_observable_changed(self):
        Listener(self.callback).set_observable(self.observable)
        self.callback.reset_mock()
        self.observable._notify()
        self.callback.assert_called_with(self.observable)

    def test_unregisters_on_old_observer(self):
        first_observable = Mock()
        second_observable = Mock()
        listener = Listener(self.callback)
        listener.set_observable(first_observable)
        listener.set_observable(second_observable)
        self.assertTrue(first_observable.unlisten.called)

    def setUp(self):
        self.callback = Mock()
        self.observable = Observable()


class Observer(object):

    def __init__(self):
        self.events = []

    def event_triggered(self, evt):
        self.events.append(evt)

    def event_triggered2(self):
        self.events.append(None)
