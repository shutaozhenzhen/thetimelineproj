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


from timelinelib.general.immutable import Field
from timelinelib.general.immutable import ImmutableDict
from timelinelib.general.immutable import ImmutableRecord
from timelinelib.test.cases.unit import UnitTestCase


class describe_immutable_dict(UnitTestCase):

    def test_create_maintains_immutability(self):
        mutable = {"a": 10}
        immutable = ImmutableDict(mutable)
        mutable["a"] = 11
        self.assertEqual(mutable, {"a": 11})
        self.assertEqual(immutable, ImmutableDict(a=10))

    def test_update_maintains_immutability(self):
        mutable = {"a": 2, "b": 4}
        immutable1 = ImmutableDict(mutable)
        immutable2 = immutable1.update(b=5)
        self.assertEqual(mutable, {"a": 2, "b": 4})
        self.assertEqual(immutable1, ImmutableDict(a=2, b=4))
        self.assertEqual(immutable2, ImmutableDict(a=2, b=5))

    def test_remove_maintains_immutability(self):
        mutable = {"a": 10, "b": 11}
        immutable1 = ImmutableDict(mutable)
        immutable2 = immutable1.remove("a")
        self.assertEqual(mutable, {"a": 10, "b": 11})
        self.assertEqual(immutable1, ImmutableDict(a=10, b=11))
        self.assertEqual(immutable2, ImmutableDict(b=11))

    def test_map_maintains_immutability(self):
        mutable = {"a": 2, "b": 4}
        immutable1 = ImmutableDict(mutable)
        immutable2 = immutable1.map(lambda x: x**2)
        self.assertEqual(mutable, {"a": 2, "b": 4})
        self.assertEqual(immutable1, ImmutableDict(a=2, b=4))
        self.assertEqual(immutable2, ImmutableDict(a=4, b=16))

    def test_contains(self):
        d = ImmutableDict(item=5)
        self.assertTrue("item" in d)
        self.assertTrue("foo" not in d)

    def test_get_item(self):
        d = ImmutableDict(item=5)
        self.assertEqual(d["item"], 5)

    def test_len(self):
        self.assertEqual(len(ImmutableDict(item=5, foo=9)), 2)


class describe_immutable_record(UnitTestCase):

    class R(ImmutableRecord):
        foo = Field(None)
        bar = Field(5)

    def test_gives_default_value(self):
        self.assertEqual(self.R().foo, None)
        self.assertEqual(self.R().bar, 5)

    def test_can_update(self):
        r = self.R()
        self.assertEqual(r.foo, None)
        r = r.update(foo=5)
        self.assertEqual(r.foo, 5)

    def test_limits_fields(self):
        r = self.R()
        r = r.update(foo=5)
        r = r.update(bar=5)
        with self.assertRaises(ValueError):
            r.update(baz=9)

    def test_gives_error_if_field_name_is_reserved(self):
        with self.assertRaises(ValueError):
            class R(ImmutableRecord):
                get = Field(None)
