#!/usr/bin/env python
#
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


from timelinelib.test.cases.drawers import describe_drawers
import wx


TOP_LABEL = 'Top-Label'
BOTTOM_LABEL = 'Bottom-Label'
DIVIDER_LABEL = 'Divider-Label'


class describe_minor_strip_drawer(describe_drawers):
    
    def test_can_draw_divider_line(self):
        self._drawer._appearance.get_tim_scale_pos = lambda : 1
        self._drawer.draw(DIVIDER_LABEL, 1, 2)
        self.assertEqual(1, self._dc.draw_text_call_count)
        self.assertEqual(DIVIDER_LABEL, self._dc.text)
        self.assertEqual(130, self._dc.text_y)

    def test_can_draw_top_line(self):
        self._drawer._appearance.get_tim_scale_pos = lambda : 0
        self._drawer.draw(TOP_LABEL, 1, 2)
        self.assertEqual(1, self._dc.draw_text_call_count)
        self.assertEqual(TOP_LABEL, self._dc.text)
        self.assertEqual(130, self._dc.text_y)

    def test_can_draw_bottom_line(self):
        self._drawer._appearance.get_tim_scale_pos = lambda : 2
        self._drawer.draw(BOTTOM_LABEL, 1, 2)
        self.assertEqual(1, self._dc.draw_text_call_count)
        self.assertEqual(BOTTOM_LABEL, self._dc.text)
        self.assertEqual(90, self._dc.text_y - 2 * self._text_height)

    def setUp(self):
        # self.install_gettext() # Needed when test is run standalone
        self._app = wx.App()
        from timelinelib.canvas.drawing.drawers.minorstrip import MinorStripDrawer
        self._dc = self.create_dc()
        self._scene = self.create_scene(400, 300, 150)
        self._drawer = MinorStripDrawer(ParentDrawer(self._dc, self._scene))
        self._text_height = 20
    
    def tearDown(self):
        self._app.Destroy()
        
        
class ParentDrawer():
    
    def __init__(self, dc, scene):
        self.dc = dc
        self.scene = scene
        self.time_type = TimeType()
        self.appearance = Appearance()
        self._do_draw_divider_line = True
        self._do_draw_top_scale = False
        self._do_draw_bottom_scale = False
        

class TimeType():
    
    def is_weekend_day(self, time):
        return True
    
    def is_special_day(self, time):
        return False
            
            
class Appearance():
    
    def get_minor_strip_font(self):
        return '10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)'
    
    def get_time_scale_pos(self):
        return 1
    