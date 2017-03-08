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

"""Unittests of the class :doc:`Legend <timelinelib_canvas_drawing_legend>`"""


from mock import sentinel
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.drawing.legend import Legend
from timelinelib.canvas.drawing.legend import TOP_LEFT
from timelinelib.canvas.drawing.legend import BOTTOM_RIGHT
from timelinelib.canvas.drawing.legend import TOP_RIGHT


def has_property(name):
    def outer_wrapper(f):
        def wrapper(self, *args):
            self.assertTrue(str(self.legend.__class__.__dict__[name]).startswith('<property object at '))
            f(self, *args)
        return wrapper
    return outer_wrapper


class describe_legend(UnitTestCase):
    """ """

    @has_property('rect')
    def test_has_a_rect_property(self):
        self.legend.rect = sentinel.RECT
        self.assertEqual(sentinel.RECT, self.legend.rect)

    @has_property('items')
    def test_has_a_items_property(self):
        pass

    def test_can_return_list_with_content_info(self):
        legend = self.a_legend()
        self.assertEqual([
                          ('cat-1', (10, 20, 30), (7, 14, 21), 8, 358, (92, 358, 10, 10)),
                          ('cat-2', (10, 20, 20), (7, 14, 14), 8, 371, (92, 371, 10, 10))], legend.items)

    def test_can_move_legend_to_top_of_screen(self):
        legend = self.a_legend()
        legend.pos = TOP_LEFT
        self.assertEqual([
                          ('cat-1', (10, 20, 30), (7, 14, 21), 8, 8, (92, 8, 10, 10)),
                          ('cat-2', (10, 20, 20), (7, 14, 14), 8, 21, (92, 21, 10, 10))], legend.items)

    def test_can_move_legend_to_top_right_of_screen(self):
        legend = self.a_legend()
        legend.pos = TOP_RIGHT
        self.assertEqual([
                          ('cat-1', (10, 20, 30), (7, 14, 21), 298, 8, (382, 8, 10, 10)),
                          ('cat-2', (10, 20, 20), (7, 14, 14), 298, 21, (382, 21, 10, 10))], legend.items)

    def test_can_move_legend_to_bottom_right_of_screen(self):
        legend = self.a_legend()
        legend.pos = BOTTOM_RIGHT
        self.assertEqual([
                          ('cat-1', (10, 20, 30), (7, 14, 21), 298, 358, (382, 358, 10, 10)),
                          ('cat-2', (10, 20, 20), (7, 14, 14), 298, 371, (382, 371, 10, 10))], legend.items)

    def a_legend(self):
        categories = [Cat('cat-1', (10, 20, 30)), Cat('cat-2', (10, 20, 20))]
        rect = Rect(2, 400, 100, 40)
        itemheight = 10
        legend = Legend(rect, itemheight, categories, 400, 400)
        return legend

    def setUp(self):
        self.legend = self.a_legend()


class Cat(object):

    def __init__(self, name, color):
        self.name = name
        self.color = color


class Rect():

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.Width = w
        self.width = w
        self.height = h

    def SetX(self, x):
        self.x = x

    def SetY(self, y):
        self.y = y
