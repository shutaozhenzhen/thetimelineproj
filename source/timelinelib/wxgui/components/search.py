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


import os.path

import wx

from timelinelib.config.paths import ICONS_DIR
from timelinelib.wxgui.dialogs.eventlist.view import EventListDialog


class GuiCreator(object):

    def _create_gui(self):
        self.icon_size = (16, 16)
        self._create_close_button()
        self._create_search_box()
        self._create_prev_button()
        self._create_next_button()
        self._create_list_button()
        self._create_period_button()
        self._create_no_match_label()
        self._create_single_match_label()
        self.Realize()
        self.lbl_no_match.Show(False)
        self.lbl_single_match.Show(False)
        
    def set_focus(self):
        self.search.SetFocus()

    def set_period_selections(self, values):
        if values:
            self.period.Clear()
            for value in values:
                self.period.Append(value)
            self.period.SetSelection(0)
            self.period.Show(True)
            self.period_label.Show(True)
        else:
            self.period.Show(False)
            self.period_label.Show(False)
            
    def _create_search_box(self):
        self.search = wx.SearchCtrl(self, size=(150, -1),
                                    style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN,
                  self._search_on_search_btn, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self._search_on_text_enter, self.search)
        self.AddControl(self.search)

    def _create_close_button(self):
        if 'wxMSW' in wx.PlatformInfo:
            close_bmp = wx.Bitmap(os.path.join(ICONS_DIR, "close.png"))
        else:
            close_bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, self.icon_size)
        self.AddLabelTool(wx.ID_CLOSE, "", close_bmp, shortHelp=_("Close"))
        self.Bind(wx.EVT_TOOL, self._btn_close_on_click, id=wx.ID_CLOSE)

    def _create_prev_button(self):
        prev_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR,
                                            self.icon_size)
        self.AddLabelTool(wx.ID_BACKWARD, "", prev_bmp, shortHelp=_("Prevoius match"))
        self.Bind(wx.EVT_TOOL, self._btn_prev_on_click, id=wx.ID_BACKWARD)

    def _create_next_button(self):
        next_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, self.icon_size)
        self.AddLabelTool(wx.ID_FORWARD, "", next_bmp, shortHelp=_("Next match"))
        self.Bind(wx.EVT_TOOL, self._btn_next_on_click, id=wx.ID_FORWARD)

    def _create_list_button(self):
        list_bmp = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, self.icon_size)
        self.AddLabelTool(wx.ID_MORE, "", list_bmp, shortHelp=_("List matches"))
        self.Bind(wx.EVT_TOOL, self._btn_list_on_click, id=wx.ID_MORE)

    def _create_period_button(self):
        choices = [_('Whole timeline'), _('Visible period'), _('This year')]
        self.period_label = wx.StaticText(self, wx.ID_ANY, _("In: ")) 
        self.AddControl(self.period_label)
        self.period = wx.Choice(self, wx.ID_ANY, size=(150, -1), choices=choices,
                                name = _("Select period"))
        self.Bind(wx.EVT_CHOICE, self._btn_period_on_click, self.period)
        self.AddControl(self.period)
        self.period.SetSelection(0)

    def _create_no_match_label(self):
        self.lbl_no_match = wx.StaticText(self, label=_("No match"))
        self.AddControl(self.lbl_no_match)

    def _create_single_match_label(self):
        self.lbl_single_match = wx.StaticText(self, label=_("Only one match"))
        self.AddControl(self.lbl_single_match)

    def _btn_close_on_click(self, e):
        self.Show(False)
        self.GetParent().Layout()

    def _search_on_search_btn(self, e):
        self.controller.search()

    def _search_on_text_enter(self, e):
        self.controller.search()

    def _btn_prev_on_click(self, e):
        self.controller.prev()

    def _btn_next_on_click(self, e):
        self.controller.next()

    def _btn_list_on_click(self, e):
        self.controller.list()

    def _btn_period_on_click(self, e):
        pass
    
    
class SearchBarController(object):

    def __init__(self, view):
        self.view = view
        self.result = []
        self.result_index = 0
        self.last_search = None
        self.last_period = None

    def set_timeline_canvas(self, timeline_canvas):
        self.timeline_canvas = timeline_canvas
        self.view.Enable(timeline_canvas is not None)

    def search(self):
        new_search = self.view.get_value()
        new_period = self.view.get_period()
        if (
            (self.last_search is not None and self.last_search == new_search) and 
            (self.last_period is not None and self.last_period == new_period)):
            print("Using old search")
            self.next()
        else:
            print("New search")
            self.last_search = new_search
            self.last_period = new_period
            if self.timeline_canvas is not None:
                self.result = self.timeline_canvas.get_filtered_events(new_search, new_period)
            else:
                self.result = []
            self.result_index = 0
            self.navigate_to_match()
            self.view.update_nomatch_labels(len(self.result) == 0)
            self.view.update_singlematch_label(len(self.result) == 1)
        self.view.update_buttons()

    def next(self):
        if not self._on_last_match():
            self.result_index += 1
            self.navigate_to_match()
            self.view.update_buttons()

    def prev(self):
        if not self._on_first_match():
            self.result_index -= 1
            self.navigate_to_match()
            self.view.update_buttons()

    def list(self):
        event_list = [event.get_label(self.timeline_canvas.GetTimeType()) for event in self.result]
        dlg = EventListDialog(self.view, event_list)
        if dlg.ShowModal() == wx.ID_OK:
            self.result_index = dlg.GetSelectedIndex()
            self.navigate_to_match()
        dlg.Destroy()

    def navigate_to_match(self):
        if (self.timeline_canvas is not None and self.result_index in range(len(self.result))):
            event = self.result[self.result_index]
            self.timeline_canvas.Navigate(lambda tp: tp.center(event.mean_time()))
            self.timeline_canvas.highligt_event(event, clear=True)

    def enable_backward(self):
        return bool(self.result and self.result_index > 0)

    def enable_forward(self):
        return bool(self.result and self.result_index < (len(self.result) - 1))

    def enable_list(self):
        return bool(len(self.result) > 0)

    def _on_first_match(self):
        return self.result > 0 and self.result_index == 0

    def _on_last_match(self):
        return self.result > 0 and self.result_index == (len(self.result) - 1)


class SearchBar(wx.ToolBar, GuiCreator):

    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, style=wx.TB_HORIZONTAL | wx.TB_BOTTOM)
        self.controller = SearchBarController(self)
        self._create_gui()
        self.update_buttons()

    def set_timeline_canvas(self, timeline_canvas):
        self.controller.set_timeline_canvas(timeline_canvas)

    def get_value(self):
        return self.search.GetValue()

    def get_period(self):
        return self.period.GetString(self.period.GetSelection())

    def update_nomatch_labels(self, nomatch):
        self.lbl_no_match.Show(nomatch)

    def update_singlematch_label(self, singlematch):
        self.lbl_single_match.Show(singlematch)

    def update_buttons(self):
        self.EnableTool(wx.ID_BACKWARD, self.controller.enable_backward())
        self.EnableTool(wx.ID_FORWARD, self.controller.enable_forward())
        self.EnableTool(wx.ID_MORE, self.controller.enable_list())
