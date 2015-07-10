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


from timelinelib.data.event import EXPORTABLE_FIELDS as EVENT_EXPORTABLE_FIELDS
from timelinelib.data.category import EXPORTABLE_FIELDS as CATEGORY_EXPORTABLE_FIELDS


FIELDS = {"Event": EVENT_EXPORTABLE_FIELDS, "Category": CATEGORY_EXPORTABLE_FIELDS}


class FieldSelectionDialogApi(object):
    """
    This class defines the API used by the dialog.
    """

    def on_btn_ok(self):
        try:
            self.view.close()
        except ValueError:
            pass

    def get_selected_fields(self):
        return [field[0] for field in self.view.get_fields() if field[1] is True]


class FieldSelectionDialogController(FieldSelectionDialogApi):

    def __init__(self, view, data, fields):
        FieldSelectionDialogApi.__init__(self)
        self.data = data
        self.view = view
        self._populate_view(fields)

    def _populate_view(self, fields):
        all_fields = FIELDS[self.data]
        self.view.create_field_checkboxes(all_fields, fields)
