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


import os
import wx
from timelinelib.wxgui.components.searchbar.searchbarcontroller import SearchBarController
from timelinelib.config.paths import ICONS_DIR


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
        self._search = wx.SearchCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN,
                  self._search_on_search_btn, self._search)
        self.Bind(wx.EVT_TEXT_ENTER, self._search_on_text_enter, self._search)
        self.AddControl(self._search)

    def _create_close_button(self):
        if 'wxMSW' in wx.PlatformInfo:
            close_bmp = wx.Bitmap(os.path.join(ICONS_DIR, "close.png"))
        else:
            close_bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, self._icon_size)
        self.AddLabelTool(wx.ID_CLOSE, "", close_bmp, shortHelp=_("Close"))
        self.Bind(wx.EVT_TOOL, self._btn_close_on_click, id=wx.ID_CLOSE)

    def _create_prev_button(self):
        prev_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR, self._icon_size)
        self.AddLabelTool(wx.ID_BACKWARD, "", prev_bmp, shortHelp=_("Prevoius match"))
        self.Bind(wx.EVT_TOOL, self._btn_prev_on_click, id=wx.ID_BACKWARD)

    def _create_next_button(self):
        next_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, self._icon_size)
        self.AddLabelTool(wx.ID_FORWARD, "", next_bmp, shortHelp=_("Next match"))
        self.Bind(wx.EVT_TOOL, self._btn_next_on_click, id=wx.ID_FORWARD)

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
        self._controller.Search()

    def _search_on_text_enter(self, e):
        self._controller.Search()

    def _btn_prev_on_click(self, e):
        self._controller.Prev()

    def _btn_next_on_click(self, e):
        self._controller.Next()

    def _btn_list_on_click(self, e):
        self._controller.List()

    def _btn_period_on_click(self, e):
        pass


class SearchBar(wx.ToolBar, GuiCreator):

    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, style=wx.TB_HORIZONTAL | wx.TB_BOTTOM)
        self._controller = SearchBarController(self)
        self._create_gui()
        self.UpdateButtons()

    def SetTimelineCanvas(self, timeline_canvas):
        self._controller.SetTimelineCanvas(timeline_canvas)

    def GetValue(self):
        return self._search.GetValue()

    def GetPeriod(self):
        return self._period.GetString(self._period.GetSelection())

    def UpdateNomatchLabels(self, nomatch):
        self._lbl_no_match.Show(nomatch)

    def UpdateSinglematchLabel(self, singlematch):
        self._lbl_single_match.Show(singlematch)

    def UpdateButtons(self):
        self.EnableTool(wx.ID_BACKWARD, self._controller.enable_backward())
        self.EnableTool(wx.ID_FORWARD, self._controller.enable_forward())
        self.EnableTool(wx.ID_MORE, self._controller.enable_list())
