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


CONTROL_ROWS_CREATORS = {"0": "Time details", "1": "Checkboxes",
                         "2": "Text Field", "3": "Categories listbox",
                         "4": "Container listbox", ":": "Notebook"}


class SelectTabOrderDialogController(object):

    def __init__(self, view, config):
        self.view = view
        self.config = config
        self._populate_view()

    def on_btn_ok(self):
        self._save_tab_order()
        self.view.close()

    def _populate_view(self):
        for key in self.config.event_editor_tab_order:
            self.view.append_tab_item(CONTROL_ROWS_CREATORS[key], key)
        self.view.Fit()

    def _save_tab_order(self):
        collector = []
        for i in range(len(self.config.event_editor_tab_order)):
            collector.append(self.view.get_client_data(i))
        self.config.event_editor_tab_order = "".join(collector)
