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


from mock import Mock

from timelinelib.wxgui.dialogs.eraeditors.eraseditorcontroller import ErasEditorController
from timelinelib.wxgui.dialogs.eraeditors.eraseditordialog import ErasEditorDialog
from timelinetest import UnitTestCase
from timelinetest.utils import a_gregorian_era


class describe_eras_editor(UnitTestCase):

    def test_construction(self):
        self.assertEquals(1, len(self.controller.eras))
        self.assertEquals(self.view, self.controller.view)

    def test_listbox_is_populated_at_construction(self):
        self.view.populate.assert_called_with(self.eras)

    def test_delete_removes_era(self):
        era = self.eras[0]
        self._simulate_delete_button_clicked_on(era)
        self.view.remove.assert_called_with(era)
        self.assertEquals([], self.controller.eras)

    def _simulate_delete_button_clicked_on(self, era):
        self.controller.delete(era)

    def setUp(self):
        self.eras = [a_gregorian_era()]
        self.view = Mock(ErasEditorDialog)
        self.timeline = Mock()
        self.timeline.get_all_eras.return_value = self.eras
        self.config = None
        self.controller = ErasEditorController(self.view, self.timeline, self.config)
