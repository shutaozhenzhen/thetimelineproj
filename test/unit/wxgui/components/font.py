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

import wx

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.components.font import Font
from timelinelib.wxgui.components.font import deserialize_font


class FontsTestCase(UnitTestCase):

    def setUp(self):
        self.app = wx.App()
        self.font = Font()
        self.wx_default_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    def tearDown(self):
        self.app.Destroy()


class describe_font_instantiation(FontsTestCase):

    def test_font_can_be_instatiated(self):
        self.assertTrue(self.font)

    def test_font_has_wxcolor(self):
        self.assertTrue(self.font.WxColor)

    def test_font_has_wxfont(self):
        self.assertTrue(self.font.WxFont)


class describe_font_default_values(FontsTestCase):

    def test_default_color_is_black(self):
        self.assertTrue(wx.BLACK, self.font.WxColor)

    def test_default_point_size_is_12(self):
        self.assertTrue(12, self.font.PointSize)

    def test_default_font_style_is_wx_normal(self):
        self.assertEqual(wx.FONTSTYLE_NORMAL, self.font.Style)

    def test_default_font_weight_is_wx_normal(self):
        self.assertEqual(wx.FONTWEIGHT_NORMAL, self.font.Weight)

    def test_default_font_is_not_underlined(self):
        self.assertFalse(self.font.GetUnderlined())

    def test_default_font_has_no_facename(self):
        self.assertEqual(self.wx_default_font.FaceName, self.font.FaceName)

    def test_default_font_encoding_is_wx_default(self):
        self.assertEqual(self.wx_default_font.Encoding, self.font.Encoding)


class describe_font_serialization(FontsTestCase):

    def test_font_can_be_serialized_and_deserialized(self):
        font = deserialize_font(self.font.serialize())
        self.assertEqual(self.font.PointSize, font.PointSize)
        self.assertEqual(self.font.Family, font.Family)
        self.assertEqual(self.font.Style, font.Style)
        self.assertEqual(self.font.Weight, font.Weight)
        self.assertEqual(self.font.GetUnderlined(), font.GetUnderlined())
        self.assertEqual(self.font.FaceName, font.FaceName)
        self.assertEqual(self.font.Encoding, font.Encoding)
        self.assertEqual(self.font.WxColor, font.WxColor)


class describe_font_updates(FontsTestCase):

    def test_wxcolor_can_be_changed(self):
        self.font.WxColor = wx.RED
        self.assertEqual(wx.RED, self.font.WxColor)

    def test_wxfont_can_be_changed(self):
        wxfont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                         wx.FONTWEIGHT_BOLD, True)
        self.font.WxFont = wxfont
        self.assertEqual(10, self.font.PointSize)
        self.assertEqual(wx.FONTSTYLE_ITALIC, self.font.Style)
        self.assertEqual(wx.FONTWEIGHT_BOLD, self.font.Weight)
        self.assertEqual(self.font.GetUnderlined(), wxfont.GetUnderlined())

    def test_point_size_can_be_incremented(self):
        self.font.PointSize = 12
        self.font.increment()
        self.assertEqual(14, self.font.PointSize)

    def test_point_size_can_be_decremented(self):
        self.font.PointSize = 12
        self.font.decrement()
        self.assertEqual(10, self.font.PointSize)
