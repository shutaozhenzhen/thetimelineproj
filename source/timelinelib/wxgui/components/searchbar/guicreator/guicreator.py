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

import timelinelib.wxgui.components.searchbar.guicreator.components as components


class GuiCreator(object):

    def _create_gui(self):
        self._icon_size = (16, 16)
        self._create_close_button()
        self._create_search_box()
        self._create_prev_button()
        self._create_next_button()
        self._create_list_button()
        self._create_period_button()
        self._create_no_match_label()
        self._create_single_match_label()
        self.Realize()
        self._lbl_no_match.Show(False)
        self._lbl_single_match.Show(False)
        
    def set_focus(self):
        self._search.SetFocus()

    def set_period_selections(self, values):
        if values:
            self._period.Clear()
            for value in values:
                self._period.Append(value)
            self._period.SetSelection(0)
            self._period.Show(True)
            self._period_label.Show(True)
        else:
            self._period.Show(False)
            self._period_label.Show(False)
            
    def _create_search_box(self):
        self._search = components.TextInput(self, self._search_on_search_btn)

    def _create_close_button(self):
        components.CloseButton(self, self._btn_close_on_click)

    def _create_prev_button(self):
        components.PrevButton(self, self._btn_prev_on_click)

    def _create_next_button(self):
        components.NextButton(self, self._btn_next_on_click)

    def _create_list_button(self):
        list_bmp = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, self._icon_size)
        self.AddLabelTool(wx.ID_MORE, "", list_bmp, shortHelp=_("List matches"))
        self.Bind(wx.EVT_TOOL, self._btn_list_on_click, id=wx.ID_MORE)

    def _create_period_button(self):
        choices = [_('Whole timeline'), _('Visible period'), _('This year')]
        self._period_label = wx.StaticText(self, wx.ID_ANY, _("In: ")) 
        self.AddControl(self._period_label)
        self._period = wx.Choice(self, wx.ID_ANY, size=(150, -1), choices=choices,
                                name = _("Select period"))
        self.Bind(wx.EVT_CHOICE, self._btn_period_on_click, self._period)
        self.AddControl(self._period)
        self._period.SetSelection(0)

    def _create_no_match_label(self):
        self._lbl_no_match = wx.StaticText(self, label=_("No match"))
        self.AddControl(self._lbl_no_match)

    def _create_single_match_label(self):
        self._lbl_single_match = wx.StaticText(self, label=_("Only one match"))
        self.AddControl(self._lbl_single_match)

    def _btn_close_on_click(self, e):
        self.Show(False)
        self.GetParent().Layout()

    def _search_on_search_btn(self, e):
        self._controller.search()

    def _btn_prev_on_click(self, e):
        self._controller.prev()

    def _btn_next_on_click(self, e):
        self._controller.next()

    def _btn_list_on_click(self, e):
        self._controller.list()

    def _btn_period_on_click(self, e):
        pass
