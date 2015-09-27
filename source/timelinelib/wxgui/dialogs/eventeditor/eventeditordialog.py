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


from timelinelib.db.utils import safe_locking
from timelinelib.wxgui.dialogs.editcontainerdialog.editcontainerdialog import EditContainerDialog
from timelinelib.wxgui.dialogs.editeventdialog.editeventdialog import EditEventDialog
import timelinelib.wxgui.utils as gui_utils


def open_event_editor_for(parent, config, db, handle_db_error, event):
    def create_event_editor():
        if event.is_container():
            title = _("Edit Container")
            return EditContainerDialog(parent, title, db, event)
        else:
            return EditEventDialog(
                parent, config, _("Edit Event"), db, event=event)
    def edit_function():
        gui_utils.show_modal(create_event_editor, handle_db_error)
    safe_locking(parent, edit_function)


def open_create_event_editor(parent, config, db, handle_db_error, start=None, end=None):
    def create_event_editor():
        label = _("Create Event")
        return EditEventDialog(parent, config, label, db, start, end)
    def edit_function():
        gui_utils.show_modal(create_event_editor, handle_db_error)
    safe_locking(parent, edit_function)
