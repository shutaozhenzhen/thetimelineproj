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


import os

import wx

from timelinelib.config.paths import ICONS_DIR


class ToolbarCreator(object):

    def __init__(self, frame, config):
        self.frame = frame
        self.config = config

    def create(self):
        toolbar = self.frame.CreateToolBar()
        left_tool = toolbar.AddRadioLabelTool(
            wx.ID_ANY,
            _("Left"),
            wx.Bitmap(os.path.join(ICONS_DIR, "format-justify-left.png"))
        )
        center_tool = toolbar.AddRadioLabelTool(
            wx.ID_ANY,
            _("Center"),
            wx.Bitmap(os.path.join(ICONS_DIR, "format-justify-center.png"))
        )
        def on_left_click(event):
            self.config.draw_period_events_to_right = True
        def on_center_click(event):
            self.config.draw_period_events_to_right = False
        def check_item_corresponding_to_config():
            if self.config.draw_period_events_to_right:
                toolbar.ToggleTool(left_tool.GetId(), True)
            else:
                toolbar.ToggleTool(center_tool.GetId(), True)
        self.frame.Bind(wx.EVT_TOOL, on_left_click, left_tool)
        self.frame.Bind(wx.EVT_TOOL, on_center_click, center_tool)
        self.config.listen_for_any(check_item_corresponding_to_config)
        check_item_corresponding_to_config()
        toolbar.Realize()
