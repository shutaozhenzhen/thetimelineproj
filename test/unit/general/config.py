# encoding: utf-8
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


from unittest.mock import Mock

from timelinelib.general.config import Config
from timelinelib.test.cases.tmpdir import TmpDirTestCase


class describe_config(TmpDirTestCase):

    def setUp(self):
        TmpDirTestCase.setUp(self)
        self.config = Config([
            dict(
                name="name",
                default="Rickard",
            ),
            dict(
                name="age",
                default=30,
                data_type="integer",
            ),
            dict(
                name="is_old",
                default=False,
                data_type="boolean",
            ),
            dict(
                name="other_name",
                config_name="deprecated other name",
                default="",
            ),
        ])

    def test_can_get_and_set_text(self):
        self.assertEqual(self.config.get_name(), "Rickard")
        self.config.set_name("Motörhead")
        self.assertEqual(self.config.get_name(), "Motörhead")

    def test_can_get_and_set_integer(self):
        self.assertEqual(self.config.get_age(), 30)
        self.config.set_age(18)
        self.assertEqual(self.config.get_age(), 18)

    def test_can_get_and_set_boolen(self):
        self.assertEqual(self.config.get_is_old(), False)
        self.config.set_is_old(True)
        self.assertEqual(self.config.get_is_old(), True)

    def test_can_read_from_file(self):
        with open(self.get_tmp_path("test.cfg"), "wb") as f:
            f.write(b"[DEFAULT]\n")
            f.write("name = Göran\n".encode("utf-8"))
            f.write(b"age = 3\n")
        self.config.read(self.get_tmp_path("test.cfg"))
        self.assertEqual(self.config.get_name(), "Göran")
        self.assertEqual(self.config.get_age(), 3)

    def test_specify_different_name_in_config_file(self):
        with open(self.get_tmp_path("test.cfg"), "wb") as f:
            f.write(b"[DEFAULT]\n")
            f.write(b"deprecated other name = George\n")
        self.config.read(self.get_tmp_path("test.cfg"))
        self.assertEqual(self.config.get_other_name(), "George")

    def test_calls_notify_when_set(self):
        self._notify = Mock()
        self.config.listen_for_any(self._notify)
        self.config.set_is_old(True)
        self._notify.assert_called_with()
