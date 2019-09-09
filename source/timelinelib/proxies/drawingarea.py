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


class DrawingAreaProxy:
    """
    The purpose of this proxy is to simplify the access to the canvas
    from the MainFrame window.
    
    Example of usage in MainFrame GuiCreator:
        def zoomout(evt):
            DrawingAreaProxy(self).zoom_out()
            
    Instead of writing:
        def zoomout(evt):
            self.main_panel.timeline_panel.timeline_canvas.zoom_out()
    """

    def __init__(self, creator):
        from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
        if isinstance(creator, MainFrame):
            self.timeline_canvas = creator.main_panel.timeline_panel.timeline_canvas

    def zoom_in(self):
        self.timeline_canvas.zoom_in()

    def zoom_out(self):
        self.timeline_canvas.zoom_out()

    def vertical_zoom_in(self):
        self.timeline_canvas.vertical_zoom_in()

    def vertical_zoom_out(self):
        self.timeline_canvas.vertical_zoom_out()

    @property
    def view_properties(self):
        return self.timeline_canvas.view_properties