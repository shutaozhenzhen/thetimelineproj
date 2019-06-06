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


import timelinelib.wxgui.components.searchbar.guicreator.components as components


class GuiCreator(object):

    def _create_gui(self):
        self._icon_size = (16, 16)
        self._create_components()
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
        else:
            self._period.Show(False)
            
    def _create_components(self):
        components.CloseButton(self)
        self._search = components.TextInput(self, self._search_on_search_btn)
        components.PrevButton(self, self._btn_prev_on_click)
        components.NextButton(self, self._btn_next_on_click)
        components.ShowListButton(self, self._btn_list_on_click)
        self._period = components.PeriodSelection(self, self._btn_period_on_click)
        self._lbl_no_match = components.TextLabel(self, _("No match"))
        self._lbl_single_match = components.TextLabel(self, _("Only one match"))

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
