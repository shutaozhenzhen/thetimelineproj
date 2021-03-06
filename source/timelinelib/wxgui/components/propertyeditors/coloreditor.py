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

from timelinelib.wxgui.components.propertyeditors.baseeditor import BaseEditor
from timelinelib.wxgui.components.colourselect import ColourSelect


class ColorEditorGuiCreator(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

    def create_sizer(self):
        return wx.GridBagSizer(vgap=10, hgap=10)

    def create_controls(self):
        description = wx.StaticText(self, label=_("Color used when the Event has no category associated with it."))
        self.data = self._create_color_chooser_control()
        return description, self.data

    def put_controls_in_sizer(self, sizer, controls):
        description, spin_ctrl = controls
        span = wx.GBSpan(rowspan=1, colspan=1)
        sizer.Add(description, wx.GBPosition(row=1, col=1), span)
        sizer.Add(spin_ctrl, wx.GBPosition(row=2, col=1), span)

    def _create_color_chooser_control(self):
        return ColourSelect(self)


class ColorEditor(BaseEditor, ColorEditorGuiCreator):

    def __init__(self, parent, editor, name=""):
        BaseEditor.__init__(self, parent, editor)
        ColorEditorGuiCreator.__init__(self, parent)
        self.create_gui()
        self.clear_data()

    def focus(self):
        super(ColorEditor, self).focus()

    def clear_data(self):
        self.data.SetValue(wx.LIGHT_GREY)

    def get_data(self):
        color = self.data.GetValue()
        return color.Get()
