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


from mock import Mock
import humblewx

from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.dataimport.tutorial import create_in_memory_tutorial_db
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.components.categorytree import CustomCategoryTree
from timelinelib.wxgui.framework import Dialog


class describe_custom_category_tree_component_test(UnitTestCase):

    def test_it_shows_in_dialog(self):
        self.show_dialog(TestDialog, create_in_memory_tutorial_db(), ViewProperties())


class TestDialog(Dialog):

    """
    <BoxSizerVertical>
        <CustomCategoryTree
            name="tree"
            width="300"
            height="300"
        />
    </BoxSizerVertical>
    """

    def __init__(self, db, view_properties):
        Dialog.__init__(self, humblewx.Controller, None, {
        })
        self.tree.set_timeline_view(db, view_properties)
