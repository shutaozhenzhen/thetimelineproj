# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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


import wx

from timelinelib.drawing.utils import darken_color


class CustomCategoryTree(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.renderer = CustomCategoryTreeRenderer()
        self.model = CustomCategoryTreeModel()

    def update_from_timeline_view(self, timeline_view):
        self.model.update_from_timeline_view(timeline_view)
        self.Refresh()

    def _on_size(self, event):
        self.Refresh()

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.BeginDrawing()
        (width, height) = self.GetSizeTuple()
        self.renderer.render(dc, width, height, self.model)
        dc.EndDrawing()


class CustomCategoryTreeRenderer(object):

    HEIGHT = 22
    INDENT_PX = 15
    INNER_PADDING = 2
    TRIANGLE_SIZE = 8

    def render(self, dc, width, height, model):
        self.dc = dc
        self.width = width
        self.render_entries(model.entries)
        del self.dc

    def render_entries(self, entries):
        self.y = 0
        for entry in entries:
            self.render_entry(entry)
            self.y += self.HEIGHT

    def render_entry(self, entry):
        self.render_arrow(entry.get("indent_level", 0))
        self.render_name(entry.get("name", ""), entry.get("indent_level", 0))
        self.render_color_box(entry.get("color", None))

    def render_arrow(self, indent_level):
        self.dc.SetBrush(wx.Brush(wx.Color(100, 100, 100), wx.SOLID))
        self.dc.SetPen(wx.Pen(wx.Color(100, 100, 100), 0, wx.SOLID))
        center_y = self.y + self.HEIGHT / 2
        start_x = self.INDENT_PX * indent_level + self.INNER_PADDING
        closed_polygon = [ wx.Point(start_x + self.INNER_PADDING, center_y - self.TRIANGLE_SIZE / 2)
                         , wx.Point(start_x + self.INNER_PADDING + self.TRIANGLE_SIZE, center_y)
                         , wx.Point(start_x + self.INNER_PADDING, center_y + self.TRIANGLE_SIZE / 2)
                         ]
        self.dc.DrawPolygon(closed_polygon)

    def render_name(self, name, indent_level):
        x = self.INDENT_PX * indent_level + self.TRIANGLE_SIZE + 4 * self.INNER_PADDING
        (w, h) = self.dc.GetTextExtent(name)
        self.dc.DrawText(name, x + self.INNER_PADDING, self.y + self.INNER_PADDING)

    def render_color_box(self, color):
        self.dc.SetBrush(wx.Brush(color, wx.SOLID))
        self.dc.SetPen(wx.Pen(darken_color(color), 1, wx.SOLID))
        self.dc.DrawRectangle(
            self.width - self.HEIGHT - self.INNER_PADDING,
            self.y + self.INNER_PADDING,
            self.HEIGHT - 2 * self.INNER_PADDING,
            self.HEIGHT - 2 * self.INNER_PADDING)


class CustomCategoryTreeModel(object):

    def __init__(self):
        self.entries = []

    def update_from_timeline_view(self, timeline_view):
        self.timeline_view = timeline_view
        self.update_entries()

    def get_categories(self):
        return self.timeline_view.get_timeline().get_categories()

    def is_category_visible(self, category):
        return self.timeline_view.get_view_properties().category_visible(category)

    def update_entries(self):
        self.entries = []
        self._update_from_tree(self._list_to_tree(self.get_categories()))

    def _list_to_tree(self, categories, parent=None):
        top = [category for category in categories if (category.parent == parent)]
        sorted_top = sorted(top, key=lambda category: category.name)
        return [(category, self._list_to_tree(categories, category)) for
                category in sorted_top]

    def _update_from_tree(self, category_tree, indent_level=0):
        for (category, child_tree) in category_tree:
            self.entries.append({
                "name": category.name,
                "color": category.color,
                "visible": self.is_category_visible(category),
            })
            if indent_level > 0:
                self.entries[-1]["indent_level"] = indent_level
            self._update_from_tree(child_tree, indent_level+1)
