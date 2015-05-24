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


class Font(wx.Font):

    def __init__(self, point_size=12, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL,
                 weight=wx.FONTWEIGHT_NORMAL, underlined=False, face_name="", encoding=wx.FONTENCODING_DEFAULT,
                 wxcolor=wx.BLACK):
        self.wxcolor = wxcolor
        wx.Font.__init__(self, point_size, family, style, weight, underlined, face_name, encoding)

    def _get_wxcolor(self):
        return self.wxcolor

    def _set_wxcolor(self, wxcolor):
        self.wxcolor = wxcolor

    WxColor = property(_get_wxcolor, _set_wxcolor)

    def _get_wxfont(self):
        return self

    def _set_wxfont(self, wxfont):
        self.PointSize = wxfont.PointSize
        self.Family = wxfont.Family
        self.Style = wxfont.Style
        self.Weight = wxfont.Weight
        self.Underlined = wxfont.Underlined
        self.FaceName = wxfont.FaceName
        self.Encoding = wxfont.Encoding

    WxFont = property(_get_wxfont, _set_wxfont)

    def serialize(self):
        return "%s:%s:%s:%s:%s:%s:%s:%s" % (self.PointSize, self.Family, self.Style, self.Weight,
                                            self.Underlined, self.FaceName, self.Encoding, self.WxColor)

    def increment(self, step=2):
        self.PointSize += step

    def decrement(self, step=2):
        self.PointSize -= step


def deserialize_font(serialized_font):
    bool_map = {"True": True, "False": False}
    point_size, family, style, weight, underlined, facename, encoding, color = serialized_font.split(":")
    color_args = color[1:-1].split(",")
    wxcolor = wx.Color(int(color_args[0]), int(color_args[1]), int(color_args[2]), int(color_args[3]))
    return Font(int(point_size), int(family), int(style), int(weight), bool_map[underlined], facename, int(encoding), wxcolor)


def set_minor_strip_text_font(config, dc, force_bold=False, force_normal=False):
    set_text_font(config.minor_strip_font, dc, force_bold, force_normal)


def set_major_strip_text_font(config, dc, force_bold=False, force_normal=False):
    set_text_font(config.major_strip_font, dc, force_bold, force_normal)


def set_legend_text_font(config, dc):
    set_text_font(config.legend_font, dc)


def set_text_font(selectable_font, dc, force_bold=False, force_normal=False):
    font = deserialize_font(selectable_font)
    if force_bold:
        font.Weight = wx.FONTWEIGHT_BOLD
    elif force_normal:
        font.Weight = wx.FONTWEIGHT_NORMAL
    dc.SetFont(font)
    dc.SetTextForeground(font.WxColor)


def get_default_font(size, bold=False):
    if bold:
        weight = wx.FONTWEIGHT_BOLD
    else:
        weight = wx.FONTWEIGHT_NORMAL
    return Font(size, weight=weight)
