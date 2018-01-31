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

"""
Contains tests of the class 
:doc:`GraphObject <timelinelib_canvas_drawing_graphobject>`.
"""


from mock import Mock
from mock import sentinel
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.drawing.graphobject import GraphObject


def has_property(name):
    def outer_wrapper(f):
        def wrapper(self, *args):
            self.assertTrue(str(self.go.__class__.__dict__[name]).startswith('<property object at '))
            f(self, *args)
        return wrapper
    return outer_wrapper


def autodoc(f):
    def wrapper(*args):
        """ """
        f(*args)
    return wrapper


class describe_graphobject(UnitTestCase):
    """ """

    @autodoc
    def test_can_be_translated(self):
        self.go.translate(10, 20)
        self.assertEqual((20, 40), self.go.point)

    @autodoc
    def test_when_translated_all_childs_are_translated(self):
        self.go.translate(10, 10)
        for c in self.go.childs:
            c.translate.assert_called_with(10, 10)

    @autodoc
    @has_property('text')
    def test_has_property_text(self):
        self.assertEqual('foobar', self.go.text)

    @autodoc
    @has_property('point')
    def test_has_property_point(self):
        self.assertEqual((10, 20), self.go.point)

    @autodoc
    @has_property('rect')
    def test_has_property_rect(self):
        self.assertEqual((10, 20, 100, 50), self.go.rect)

    @autodoc
    @has_property('width')
    def test_has_property_width(self):
        self.assertEqual(100, self.go.width)

    @autodoc
    @has_property('height')
    def test_has_property_height(self):
        self.assertEqual(50, self.go.height)

    @autodoc
    @has_property('brush_color')
    def test_has_property_brush_color(self):
        self.go.brush_color = sentinel.BRUSH_COLOR
        self.assertEqual(sentinel.BRUSH_COLOR, self.go.brush_color)

    @autodoc
    @has_property('pen_color')
    def test_has_property_pen_color(self):
        self.go.pen_color = sentinel.PEN_COLOR
        self.assertEqual(sentinel.PEN_COLOR, self.go.pen_color)

    @autodoc
    @has_property('childs')
    def test_has_property_childs(self):
        self.go.childs = sentinel.CHILDS
        self.assertEqual(sentinel.CHILDS, self.go.childs)

    @autodoc
    @has_property('first_child')
    def test_has_property_first_child(self):
        self.assertEqual(self.childs[0], self.go.first_child)

    @autodoc
    def test_a_child_can_be_added(self):
        self.go.add_child(sentinel.CHILD)
        self.assertEqual(3, len(self.go.childs))
        self.assertEqual(sentinel.CHILD, self.go.childs[-1])

    def setUp(self):
        self.go = GraphObject(x=10, y=20, w=100, h=50, text='foobar')
        self.childs = [Mock(GraphObject), Mock(GraphObject)]
        self.go.childs = self.childs
