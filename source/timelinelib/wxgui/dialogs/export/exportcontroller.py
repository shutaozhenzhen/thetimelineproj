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


from timelinelib.wxgui.dialogs.fieldselectiondialog.fieldselectiondialogcontroller import FIELDS


CSV_FILE = _("CSV File")
TARGET_TYPES = (CSV_FILE,)
TEXT_ENCODINGS = ("utf-8", "cp1252", "cp850")


class ExportDialogApi(object):
    """
    This class defines the API used by the dialog.
    """

    def on_btn_ok(self):
        try:
            if self._validate_input():
                self.view.close()
        except ValueError:
            pass

    def _validate_input(self):
        if not self.view.get_export_events() and not self.view.get_export_categories():
            self.view.display_information_message(_("Invalid Data"), _("At least one Export Item must be selected"))
            return False
        if self.view.get_export_events() and self.event_fields == []:
            self.view.display_information_message(_("Invalid Data"), _("At least one Event Field must be selected"))
            return False
        if self.view.get_export_categories() and self.category_fields == []:
            self.view.display_information_message(_("Invalid Data"), _("At least one Category Field must be selected"))
            return False
        return True

    def set_event_fields(self, fields):
        self.event_fields = fields

    def set_category_fields(self, fields):
        self.category_fields = fields

    def get_event_fields(self):
        return self.event_fields

    def get_category_fields(self):
        return self.category_fields


class ExportController(ExportDialogApi):
    """
    This class is the dialog controller.

    It populates the dialog at startup and it validates the
    entered data before it closes the dialog.
    """

    def __init__(self, view):
        ExportDialogApi.__init__(self)
        self.view = view
        self.event_fields = FIELDS["Event"]
        self.category_fields = FIELDS["Category"]
        self._populate_view()

    def _populate_view(self):
        self.view.set_target_types(TARGET_TYPES)
        self.view.set_text_encodings(TEXT_ENCODINGS)
        self.view.set_events(False)
        self.view.set_categories(False)
