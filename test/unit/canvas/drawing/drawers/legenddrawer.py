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

"""
Contains tests of the class 
:doc:`LegendDrawer <timelinelib_canvas_drawing_drawers_legenddrawer>`.
"""


from mock import Mock
from mock import sentinel
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.canvas.drawing.drawers.legenddrawer import LegendDrawer
from timelinelib.canvas.drawing.graphobject import GraphObject


def autodoc(f):
    def wrapper(*args):
        """ """
        f(*args)
    return wrapper


class describe_legend_drawer(UnitTestCase):
    """ """

    @autodoc
    def test_set_legend_pos_0(self):
        self.scene._view_properties.legend_pos = 0
        go = self.a_graph_object_with(w=10, h=30)
        self.drawer._set_legend_pos(go)
        go.translate.assert_called_with(0, 10)

    @autodoc
    def test_set_legend_pos_1(self):
        self.scene._view_properties.legend_pos = 1
        go = self.a_graph_object_with(w=10, h=30)
        self.drawer._set_legend_pos(go)
        go.translate.assert_called_with(0, 0)

    @autodoc
    def test_set_legend_pos_2(self):
        self.scene._view_properties.legend_pos = 2
        go = self.a_graph_object_with(w=10, h=30)
        self.drawer._set_legend_pos(go)
        go.translate.assert_called_with(80, 0)

    @autodoc
    def test_set_legend_pos_3(self):
        self.scene._view_properties.legend_pos = 3
        go = self.a_graph_object_with(w=10, h=30)
        self.drawer._set_legend_pos(go)
        go.translate.assert_called_with(80, 10)

    def a_graph_object_with(self, w=0, h=0):
        go = Mock(GraphObject)
        go.width = w
        go.height = h
        return go

    def setUp(self):
        self.dc = Mock()
        self.scene = Mock()
        self.scene.width = 100
        self.scene.height = 50
        self.scene._view_properties.legend_pos = 1
        self.categories = Mock()
        self.drawer = LegendDrawer(self.dc, self.scene, self.categories)
