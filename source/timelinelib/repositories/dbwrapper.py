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


from timelinelib.repositories.interface import CategoryRepository
from timelinelib.repositories.interface import EventRepository
from timelinelib.canvas.data import sort_categories


class DbWrapperCategoryRepository(CategoryRepository):

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.get_categories()

    def get_tree(self, remove):
        return category_tree(self.get_all(), remove=remove)

    def save(self, category):
        self.db.save_category(category)


class DbWrapperEventRepository(EventRepository):

    def __init__(self, db):
        self.db = db

    def save(self, event):
        self.db.save_event(event)


def category_tree(category_list, parent=None, remove=None):
    """
    Transform flat list of categories to a tree based on parent attribute.

    The top-level categories have the given parent and each level in the tree
    is sorted.

    If remove is given then the subtree with remove as root will not be
    included.

    The tree is represented as a list of tuples, (cat, sub-tree), where cat is
    the parent category and subtree is the same tree representation of the
    children.
    """
    children = [child for child in category_list
                if (child.parent == parent and child != remove)]
    sorted_children = sort_categories(children)
    tree = [(x, category_tree(category_list, x, remove))
            for x in sorted_children]
    return tree
