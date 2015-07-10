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


import os.path

import wx

from timelinelib.wxgui.utils import BORDER
from timelinelib.config.paths import ICONS_DIR
from timelinelib.wxgui.dialogs.eventeditor.eventeditortabselectioncontroller import SelectTabOrderDialogController


UP = 0
DOWN = 1


class SelectTabOrderGuiCreator(object):

    def _create_gui(self):
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        self._add_input_controls(box_sizer)
        self._add_buttons(box_sizer)
        self.SetSizerAndFit(box_sizer)

    def _add_input_controls(self, sizer):
        tab_order_selector = self._create_tab_order_selector()
        sizer.Add(tab_order_selector, flag=wx.EXPAND | wx.ALL, border=BORDER, proportion=1)

    def _add_buttons(self, properties_box):
        button_box = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        properties_box.Add(button_box, flag=wx.ALL, border=BORDER)
        self.Bind(wx.EVT_BUTTON, self._btn_ok_on_click, id=wx.ID_OK)

    def _create_tab_order_selector(self):
        self.lst_tab_order = wx.ListBox(self, wx.ID_ANY)
        label = wx.StaticText(self, label=_("Select Tab Order:"))
        self._btn_up = self._create_up_button()
        self._btn_down = self._create_down_button()
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.Add(self._btn_up, flag=wx.ALL, border=BORDER)
        button_sizer.Add(self._btn_down, flag=wx.ALL, border=BORDER)
        list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_sizer.Add(self.lst_tab_order)
        list_sizer.Add(button_sizer, border=BORDER)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer.Add(label, flag=wx.ALL, border=BORDER)
        panel_sizer.Add(list_sizer)
        self.Bind(wx.EVT_LISTBOX, self._on_list_item_selected, self.lst_tab_order)
        return panel_sizer

    def _create_up_button(self):
        return self._create_bitmap_button(wx.ART_GO_UP)

    def _create_down_button(self):
        return self._create_bitmap_button(wx.ART_GO_DOWN)

    def _create_bitmap_button(self, bitmap_id):
        bmp = self._get_bitmap(bitmap_id)
        btn = wx.BitmapButton(self, wx.ID_ANY, bmp, (20, 20), (bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        btn.Disable()
        self.Bind(wx.EVT_BUTTON, self._on_button_up_or_down_click, btn)
        return btn

    def _get_bitmap(self, bitmap_id):
        if 'wxMSW' in wx.PlatformInfo:
            name = {wx.ART_GO_UP: "up.png", wx.ART_GO_DOWN: "down.png"}
            return wx.Bitmap(os.path.join(ICONS_DIR, name[bitmap_id]))
        else:
            size = (24, 24)
            return wx.ArtProvider.GetBitmap(bitmap_id, wx.ART_TOOLBAR, size)


class SelectTabOrderDialog(wx.Dialog, SelectTabOrderGuiCreator):

    def __init__(self, parent, config):
        self.config = config
        title = _("Event Editor Tab Order")
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, parent, title=title, name="select_event_editor_tab_order", style=style)
        self._create_gui()
        self.controller = SelectTabOrderDialogController(self, config)

    def _on_list_item_selected(self, evt):
        self._btn_up.Enable()
        self._btn_down.Enable()

    def _btn_ok_on_click(self, evt):
        self.controller.on_btn_ok()

    def _on_button_up_or_down_click(self, evt):
        inx = self.lst_tab_order.GetSelection()
        if evt.EventObject == self._btn_up:
            if inx > 0:
                self._move_list_row(inx, UP)
        else:
            if inx < self.lst_tab_order.GetCount() - 1:
                self._move_list_row(inx, DOWN)

    def _move_list_row(self, inx, direction):
        text = self.lst_tab_order.GetString(inx)
        key = self.lst_tab_order.GetClientData(inx)
        self.lst_tab_order.Delete(inx)
        if direction == UP:
            inx -= 1
        else:
            inx += 1
        self.lst_tab_order.Insert(text, inx, key)
        self.lst_tab_order.Select(inx)

    def append_tab_item(self, text, client_data):
        self.lst_tab_order.Append(text, client_data)

    def get_client_data(self, inx):
        return self.lst_tab_order.GetClientData(inx)

    def close(self):
        self.EndModal(wx.ID_OK)
